import httpx
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    def _titles_similar(self, title1: str, title2: str) -> bool:
        """
        Check if two titles are >80% similar using Jaccard similarity
        
        Args:
            title1: First article title
            title2: Second article title
            
        Returns:
            True if titles are similar (>80% word overlap)
        """
        words1 = set(title1.lower().split())
        words2 = set(title2.lower().split())
        if not words1 or not words2:
            return False
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        similarity = len(intersection) / len(union)
        return similarity > 0.8
    
    async def _fetch_articles_by_day(
        self,
        client: httpx.AsyncClient,
        from_date: str,
        to_date: str,
        limit_per_day: int = 15
    ) -> List[Dict]:
        """
        Fetch articles by making multiple requests, one per day, to ensure
        we get articles from all days in the range.
        
        Args:
            client: HTTPX async client
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            limit_per_day: Number of articles to fetch per day
            
        Returns:
            List of article dictionaries (not yet processed)
        """
        # Parse dates
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        
        # Calculate days in range
        days_diff = (to_dt - from_dt).days + 1
        
        print(f"📅 Fetching articles day-by-day from {days_diff} days ({from_date} to {to_date})")
        
        all_raw_articles = []
        
        # Fetch articles day by day
        for i in range(days_diff):
            current_date = (from_dt + timedelta(days=i)).strftime("%Y-%m-%d")
            
            try:
                params = {
                    "apiKey": self.api_key,
                    "q": "(technology OR tech OR AI OR startup OR software OR hardware OR mobile OR cloud OR security OR robotics OR gaming) AND (announcement OR launch OR release OR update OR report OR news)",
                    "language": "en",
                    "sortBy": "publishedAt",
                    "from": current_date,
                    "to": current_date,
                    "pageSize": min(20, limit_per_day * 4),  # Fetch 4x per day for better selection
                    "domains": "techcrunch.com,theverge.com,wired.com,arstechnica.com,engadget.com,cnet.com,zdnet.com,mashable.com,theguardian.com,bbc.com,reuters.com"
                }
                
                url = f"{self.base_url}/everything"
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                day_articles = data.get("articles", [])
                print(f"  ✓ {current_date}: Found {len(day_articles)} raw articles")
                all_raw_articles.extend(day_articles)
                
            except Exception as e:
                print(f"  ⚠️ {current_date}: Error fetching - {str(e)}")
                continue
        
        return all_raw_articles
    
    async def fetch_top_tech_news(
        self, 
        limit: int = 10,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Fetch tech news from NewsAPI
        Uses /everything for date ranges, /top-headlines for recent news
        
        Args:
            limit: Number of articles to fetch (max 100)
            from_date: Filter articles published on or after this date (YYYY-MM-DD string)
            to_date: Filter articles published on or before this date (YYYY-MM-DD string)
            
        Returns:
            List of unique article dictionaries
        """
        async with httpx.AsyncClient() as client:
            # CRITICAL: Use different endpoints based on date filtering
            if from_date or to_date:
                # Calculate default dates if not provided
                if not to_date:
                    to_date = datetime.now().strftime("%Y-%m-%d")
                if not from_date:
                    # Default to 7 days ago if only to_date provided
                    from_dt = datetime.now() - timedelta(days=7)
                    from_date = from_dt.strftime("%Y-%m-%d")
                
                # Calculate days in range
                from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                days_diff = (to_dt - from_dt).days + 1
                
                # For ranges of 5+ days, fetch day-by-day to ensure coverage
                # This ensures we get articles from ALL days, not just the most recent
                if days_diff >= 5:
                    print(f"🔄 Using day-by-day fetching for {days_diff} day range")
                    raw_articles = await self._fetch_articles_by_day(
                        client, from_date, to_date, limit_per_day=15
                    )
                    # Process raw articles
                    data = {"articles": raw_articles}
                else:
                    # For shorter ranges, use single request
                    url = f"{self.base_url}/everything"
                    params = {
                        "apiKey": self.api_key,
                        "q": "(technology OR tech OR AI OR startup OR software OR hardware) AND (announcement OR launch OR release OR update OR report)",
                        "language": "en",
                        "sortBy": "publishedAt",
                        "from": from_date,
                        "to": to_date,
                        "pageSize": min(100, limit * 10),  # Fetch 10x target, max 100
                        "domains": "techcrunch.com,theverge.com,wired.com,arstechnica.com,engadget.com,cnet.com,zdnet.com,mashable.com"
                    }
                    
                    print(f"🔍 Fetching from: {url}")
                    print(f"📅 Date range: {from_date} to {to_date}")
                    
                    response = await client.get(url, params=params, timeout=30.0)
                    response.raise_for_status()
                    data = response.json()
            else:
                # Use /top-headlines for recent news (last 24h)
                url = f"{self.base_url}/top-headlines"
                params = {
                    "apiKey": self.api_key,
                    "category": "technology",
                    "language": "en",
                    "pageSize": limit
                }
                
                print(f"🔍 Fetching from: {url}")
                print(f"📅 Recent news (24h)")
                
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
            
            articles = []
            seen_urls = set()
            seen_titles = []
            
            for article in data.get("articles", []):
                # Skip if no URL
                if not article.get("url"):
                    continue
                
                # Deduplication by URL
                if article["url"] in seen_urls:
                    print(f"⚠️ Duplicate URL: {article.get('title', '')[:50]}...")
                    continue
                
                # Deduplication by similar title
                title = article.get("title", "")
                is_duplicate = False
                for seen_title in seen_titles:
                    if self._titles_similar(title, seen_title):
                        print(f"⚠️ Similar title: {title[:50]}...")
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    continue
                
                # Generate unique ID
                article_id = hashlib.md5(article["url"].encode()).hexdigest()[:12]
                
                # Add to unique articles
                articles.append({
                    "id": article_id,
                    "title": title,
                    "description": article.get("description", ""),
                    "url": article["url"],
                    "source": article["source"]["name"],
                    "publishedAt": article["publishedAt"],
                    "imageUrl": article.get("urlToImage")
                })
                
                seen_urls.add(article["url"])
                seen_titles.append(title)
                
                # Don't stop early - we need all articles for intelligent sampling
                # Only stop if we've processed all available articles
            
            print(f"✅ Total unique articles after dedup: {len(articles)}")
            
            # ALWAYS apply sampling when date range exists (not just when articles > limit)
            if from_date or to_date:
                print(f"🎯 Applying intelligent sampling: {len(articles)} → {limit}")
                sampled = self._sample_articles_intelligently(
                    articles, 
                    limit,
                    from_date,
                    to_date
                )
                print(f"✅ After sampling: {len(sampled)} articles")
                return sampled
            
            # For recent news (no dates), just return top scored articles
            if len(articles) > limit:
                print(f"🎯 Scoring and selecting top {limit} articles")
                scored = self._score_articles(articles)
                return scored[:limit]
            
            return articles
    
    def _score_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Score articles by importance/quality.
        
        Scoring factors:
        - Source quality (tier 1 sources = higher score)
        - Recency (newer = slightly higher)
        - Content quality (has description, image)
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            List of articles sorted by score (highest first)
        """
        tier1_sources = {
            "TechCrunch", "The Verge", "Wired", "Ars Technica", 
            "Engadget", "CNET", "ZDNet", "Reuters", "Bloomberg",
            "MIT Technology Review", "IEEE Spectrum"
        }
        
        tier2_sources = {
            "Mashable", "VentureBeat", "TechRadar", "PCMag",
            "Digital Trends", "Tom's Hardware", "AnandTech"
        }
        
        scored_articles = []
        for article in articles:
            score = 0
            
            # Source quality (biggest factor)
            source = article.get("source", "")
            if source in tier1_sources:
                score += 10
            elif source in tier2_sources:
                score += 5
            else:
                score += 1
            
            # Has good description
            desc = article.get("description", "")
            if desc and len(desc) > 100:
                score += 3
            elif desc and len(desc) > 50:
                score += 1
            
            # Has image
            if article.get("imageUrl"):
                score += 2
            
            # Title quality (not too short, not "[Removed]")
            title = article.get("title", "")
            if title and len(title) > 30 and "[Removed]" not in title:
                score += 2
            
            # Recency bonus (slight preference for newer)
            try:
                pub_date = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                hours_old = (datetime.now(pub_date.tzinfo) - pub_date).total_seconds() / 3600
                if hours_old < 6:
                    score += 2
                elif hours_old < 12:
                    score += 1
            except:
                pass
            
            scored_articles.append((score, article))
        
        # Sort by score (highest first) and return articles only
        scored_articles.sort(key=lambda x: x[0], reverse=True)
        return [article for score, article in scored_articles]
    
    def _sample_articles_intelligently(
        self, 
        articles: List[Dict], 
        target_count: int,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Sample articles to ensure even distribution across days
        
        Args:
            articles: List of article dictionaries
            target_count: Target number of articles to return
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
            
        Returns:
            List of sampled articles
        """
        if not articles:
            return []
        
        # Group by day
        by_day = defaultdict(list)
        for article in articles:
            try:
                # Extract date from publishedAt (YYYY-MM-DDTHH:MM:SSZ)
                pub_date = article["publishedAt"][:10]  # YYYY-MM-DD
                by_day[pub_date].append(article)
            except:
                # If date parsing fails, add to a default bucket
                by_day["unknown"].append(article)
        
        print(f"📊 Grouped into {len(by_day)} days:")
        for day in sorted(by_day.keys()):
            print(f"  {day}: {len(by_day[day])} articles")
        
        # Calculate articles per day
        days_count = len(by_day)
        if days_count == 0:
            return articles[:target_count]
        
        per_day = max(1, target_count // days_count)
        extra = target_count % days_count
        
        print(f"🎯 Taking {per_day} per day + {extra} extra")
        
        # Sample from each day
        result = []
        sorted_days = sorted(by_day.keys(), reverse=True)  # Newest first
        
        for i, day in enumerate(sorted_days):
            day_articles = by_day[day]
            
            # Score articles for this day
            scored = self._score_articles(day_articles)
            
            # How many to take from this day
            take = per_day
            if i < extra:  # Distribute extra articles to first N days
                take += 1
            
            # Take top articles
            selected = scored[:take]
            result.extend(selected)
            
            print(f"  ✓ {day}: Selected {len(selected)} of {len(day_articles)}")
        
        return result[:target_count]

