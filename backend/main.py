from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Dict, Optional

from models.schemas import Article, NewsResponse, HealthResponse
from services.news_service import NewsService
from services.ai_service import AIService

# Load environment variables
load_dotenv()

# Global cache
cache: Dict = {
    "articles": [],
    "timestamp": None,
    "ttl": int(os.getenv("CACHE_TTL", 900))  # 15 minutes default
}

# Initialize services
news_service = NewsService(api_key=os.getenv("NEWS_API_KEY"))
ai_service = AIService(api_key=os.getenv("OPENAI_API_KEY"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("🚀 Starting Tech News Summarizer API")
    print(f"📦 Cache TTL: {cache['ttl']} seconds")
    yield
    print("👋 Shutting down API")

# Create FastAPI app
app = FastAPI(
    title="Tech News Summarizer API",
    description="AI-powered tech news summarization service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_cache_valid() -> bool:
    """Check if cache is still valid"""
    if not cache["timestamp"] or not cache["articles"]:
        return False
    
    age = (datetime.now() - cache["timestamp"]).total_seconds()
    return age < cache["ttl"]

def get_cache_age() -> Optional[int]:
    """Get cache age in seconds"""
    if not cache["timestamp"]:
        return None
    return int((datetime.now() - cache["timestamp"]).total_seconds())

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Tech News Summarizer API",
        "version": "1.0.0",
        "endpoints": {
            "news": "/api/news",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        cache_size=len(cache["articles"]),
        cache_age_seconds=get_cache_age()
    )

@app.get("/api/news", response_model=NewsResponse)
async def get_news(limit: int = 10, force_refresh: bool = False):
    """
    Get latest tech news with AI summaries
    
    Args:
        limit: Number of articles to return (1-100)
        force_refresh: Force cache refresh
        
    Returns:
        NewsResponse with articles and metadata
    """
    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    # Check cache
    if is_cache_valid() and not force_refresh:
        print("📦 Returning cached results")
        return NewsResponse(
            articles=cache["articles"][:limit],
            count=len(cache["articles"][:limit]),
            cached=True,
            cache_age=get_cache_age()
        )
    
    print("🔄 Fetching fresh news...")
    
    try:
        # Fetch news from NewsAPI
        articles = await news_service.fetch_top_tech_news(limit=limit)
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found")
        
        print(f"📰 Fetched {len(articles)} articles")
        print("🤖 Generating AI summaries...")
        
        # Generate AI summaries
        summarized_articles = await ai_service.summarize_articles_batch(articles)
        
        # Update cache
        cache["articles"] = [Article(**article) for article in summarized_articles]
        cache["timestamp"] = datetime.now()
        
        print(f"✅ Successfully processed {len(summarized_articles)} articles")
        
        return NewsResponse(
            articles=cache["articles"][:limit],
            count=len(cache["articles"][:limit]),
            cached=False,
            cache_age=0
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.post("/api/refresh")
async def refresh_cache():
    """Force refresh the news cache"""
    cache["articles"] = []
    cache["timestamp"] = None
    return {"message": "Cache cleared", "status": "success"}

@app.get("/api/news/{article_id}", response_model=Article)
async def get_article(article_id: str):
    """Get a specific article by ID"""
    if not cache["articles"]:
        raise HTTPException(status_code=404, detail="No articles in cache")
    
    for article in cache["articles"]:
        if article.id == article_id:
            return article
    
    raise HTTPException(status_code=404, detail="Article not found")

# Run with: uvicorn main:app --reload

