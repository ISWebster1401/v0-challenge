import httpx
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional

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
                # Use /everything for historical data
                url = f"{self.base_url}/everything"
                
                # Calculate default dates if not provided
                if not to_date:
                    to_date = datetime.now().strftime("%Y-%m-%d")
                if not from_date:
                    # Default to 7 days ago if only to_date provided
                    from_dt = datetime.now() - timedelta(days=7)
                    from_date = from_dt.strftime("%Y-%m-%d")
                
                params = {
                    "apiKey": self.api_key,
                    "q": "(technology OR tech OR AI OR startup OR software OR hardware) AND (announcement OR launch OR release OR update OR report)",
                    "language": "en",
                    "sortBy": "publishedAt",
                    "from": from_date,
                    "to": to_date,
                    "pageSize": min(limit * 3, 100),  # Fetch 3x more for deduplication
                    "domains": "techcrunch.com,theverge.com,wired.com,arstechnica.com,engadget.com,cnet.com,zdnet.com,mashable.com"
                }
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
            print(f"📅 Date range: {from_date} to {to_date}" if from_date else "📅 Recent news (24h)")
            
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
                
                # Stop when we have enough unique articles
                if len(articles) >= limit:
                    break
            
            print(f"✅ Fetched {len(articles)} unique articles (from {len(data.get('articles', []))} total)")
            return articles

