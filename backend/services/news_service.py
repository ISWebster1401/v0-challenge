import httpx
import hashlib
from datetime import datetime
from typing import List, Dict, Optional

class NewsService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    async def fetch_top_tech_news(self, limit: int = 10) -> List[Dict]:
        """
        Fetch top tech news from NewsAPI
        
        Args:
            limit: Number of articles to fetch (max 100)
            
        Returns:
            List of article dictionaries
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/top-headlines",
                params={
                    "apiKey": self.api_key,
                    "category": "technology",
                    "language": "en",
                    "pageSize": limit
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get("articles", []):
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
            
            return articles

