import httpx
import hashlib
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    async def fetch_top_tech_news(self, limit: int = 10, from_date: Optional[date] = None, to_date: Optional[date] = None) -> List[Dict]:
        """
        Fetch top tech news from NewsAPI with optional date filtering
        
        Args:
            limit: Number of articles to fetch (max 100)
            from_date: Filter articles published on or after this date (YYYY-MM-DD)
            to_date: Filter articles published on or before this date (YYYY-MM-DD)
            
        Returns:
            List of article dictionaries filtered by date range
        """
        # For date filtering, we need to use the 'everything' endpoint with date parameters
        # NewsAPI requires both from and to dates for date filtering
        params = {
            "apiKey": self.api_key,
            "language": "en",
            "pageSize": min(limit, 100),
            "sortBy": "publishedAt"
        }
        
        # If dates are provided, use 'everything' endpoint with date filters
        if from_date or to_date:
            # Default to last 7 days if only one date provided
            if from_date and not to_date:
                to_date = date.today()
            elif to_date and not from_date:
                # Go back 7 days from to_date
                from_date = to_date - timedelta(days=7)
            
            # Convert dates to ISO format strings
            params["from"] = from_date.isoformat()
            params["to"] = to_date.isoformat()
            params["q"] = "technology OR tech OR AI OR software OR programming"
            endpoint = f"{self.base_url}/everything"
        else:
            # No date filtering - use top-headlines
            params["category"] = "technology"
            endpoint = f"{self.base_url}/top-headlines"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                endpoint,
                params=params,
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                # Parse published date
                try:
                    published_at = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                except:
                    continue
                
                # Additional client-side date filtering if using 'everything' endpoint
                if from_date or to_date:
                    article_date = published_at.date()
                    if from_date and article_date < from_date:
                        continue
                    if to_date and article_date > to_date:
                        continue
                
                # Generate unique ID from URL
                article_id = hashlib.md5(article["url"].encode()).hexdigest()[:12]
                
                articles.append({
                    "id": article_id,
                    "title": article["title"],
                    "description": article.get("description", ""),
                    "url": article["url"],
                    "source": article["source"]["name"],
                    "publishedAt": article["publishedAt"],
                    "imageUrl": article.get("urlToImage")
                })
            
            # Limit results to requested amount
            return articles[:limit]

