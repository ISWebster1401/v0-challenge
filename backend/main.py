from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from typing import Dict, Optional
from collections import defaultdict, deque
import asyncio

from models.schemas import Article, NewsResponse, HealthResponse, FullSummaryRequest, FullSummaryResponse
from services.news_service import NewsService
from services.ai_service import AIService
from services.web_scraper import WebScraper
from services.topic_extractor import TopicExtractor

# Load environment variables
load_dotenv()

# Global cache with date-based keys
cache: Dict[str, Dict] = defaultdict(lambda: {
    "articles": [],
    "timestamp": None,
    "ttl": int(os.getenv("CACHE_TTL", 900))  # 15 minutes default
})

# Full summary cache (by URL) - 24 hour TTL
full_summary_cache: Dict[str, Dict] = {}

# Rate limiting for full summaries (10 per minute)
rate_limit_requests = deque()
RATE_LIMIT_COUNT = 10
RATE_LIMIT_WINDOW = 60  # seconds

# Initialize services
news_service = NewsService(api_key=os.getenv("NEWS_API_KEY"))
ai_service = AIService(api_key=os.getenv("OPENAI_API_KEY"))
web_scraper = WebScraper()
topic_extractor = TopicExtractor()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    print("🚀 Starting Tech News Summarizer API")
    print(f"📦 Cache TTL: {int(os.getenv('CACHE_TTL', 900))} seconds")
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

def get_cache_key(from_date: Optional[date] = None, to_date: Optional[date] = None) -> str:
    """Generate cache key based on date range"""
    if from_date and to_date:
        return f"{from_date.isoformat()}_{to_date.isoformat()}"
    elif from_date:
        return f"{from_date.isoformat()}_"
    elif to_date:
        return f"_{to_date.isoformat()}"
    return "default"

def is_cache_valid(cache_key: str) -> bool:
    """Check if cache is still valid for given key"""
    cache_entry = cache[cache_key]
    if not cache_entry["timestamp"] or not cache_entry["articles"]:
        return False
    
    age = (datetime.now() - cache_entry["timestamp"]).total_seconds()
    return age < cache_entry["ttl"]

def get_cache_age(cache_key: str) -> Optional[int]:
    """Get cache age in seconds for given key"""
    cache_entry = cache[cache_key]
    if not cache_entry["timestamp"]:
        return None
    return int((datetime.now() - cache_entry["timestamp"]).total_seconds())

def check_rate_limit() -> bool:
    """Check if rate limit allows new request"""
    now = datetime.now()
    
    # Remove requests older than the rate limit window
    while rate_limit_requests and (now - rate_limit_requests[0]).total_seconds() > RATE_LIMIT_WINDOW:
        rate_limit_requests.popleft()
    
    # Check if we're at the limit
    if len(rate_limit_requests) >= RATE_LIMIT_COUNT:
        return False
    
    # Add current request
    rate_limit_requests.append(now)
    return True

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
    total_articles = sum(len(cache[key]["articles"]) for key in cache)
    return HealthResponse(
        status="healthy",
        cache_size=total_articles,
        cache_age_seconds=None  # Multiple caches, can't provide single age
    )

@app.get("/api/news", response_model=NewsResponse)
async def get_news(
    limit: int = 10, 
    force_refresh: bool = False,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None
):
    """
    Get latest tech news with AI summaries, optionally filtered by date range
    
    Args:
        limit: Number of articles to return (1-100)
        force_refresh: Force cache refresh
        from_date: Filter articles published on or after this date (YYYY-MM-DD)
        to_date: Filter articles published on or before this date (YYYY-MM-DD)
        
    Returns:
        NewsResponse with articles and metadata
    """
    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    # Validate date range
    if from_date and to_date and from_date > to_date:
        raise HTTPException(status_code=400, detail="from_date must be before or equal to to_date")
    
    # Generate cache key based on date range
    cache_key = get_cache_key(from_date, to_date)
    
    # Check cache
    if is_cache_valid(cache_key) and not force_refresh:
        print(f"📦 Returning cached results for key: {cache_key}")
        cache_entry = cache[cache_key]
        # Extract topics from cached articles
        cached_articles_dict = [{"title": article.title} for article in cache_entry["articles"]]
        topics = topic_extractor.extract_topics(cached_articles_dict)
        return NewsResponse(
            articles=cache_entry["articles"][:limit],
            count=len(cache_entry["articles"][:limit]),
            cached=True,
            cache_age=get_cache_age(cache_key),
            topics=topics
        )
    
    date_range_str = f" from {from_date} to {to_date}" if from_date or to_date else ""
    print(f"🔄 Fetching fresh news{date_range_str}...")
    
    try:
        # Fetch news from NewsAPI with date filtering
        articles = await news_service.fetch_top_tech_news(limit=limit, from_date=from_date, to_date=to_date)
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for the specified date range")
        
        print(f"📰 Fetched {len(articles)} articles")
        print("🤖 Generating AI summaries...")
        
        # Generate AI summaries
        summarized_articles = await ai_service.summarize_articles_batch(articles)
        
        # Extract trending topics
        topics = topic_extractor.extract_topics(summarized_articles)
        print(f"📊 Extracted {len(topics)} trending topics: {', '.join(topics)}")
        
        # Update cache for this date range
        cache[cache_key]["articles"] = [Article(**article) for article in summarized_articles]
        cache[cache_key]["timestamp"] = datetime.now()
        cache[cache_key]["ttl"] = int(os.getenv("CACHE_TTL", 900))
        
        print(f"✅ Successfully processed {len(summarized_articles)} articles")
        
        return NewsResponse(
            articles=cache[cache_key]["articles"][:limit],
            count=len(cache[cache_key]["articles"][:limit]),
            cached=False,
            cache_age=0,
            topics=topics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@app.post("/api/refresh")
async def refresh_cache(from_date: Optional[date] = None, to_date: Optional[date] = None):
    """Force refresh the news cache for a specific date range"""
    cache_key = get_cache_key(from_date, to_date)
    cache[cache_key]["articles"] = []
    cache[cache_key]["timestamp"] = None
    return {"message": f"Cache cleared for date range: {cache_key}", "status": "success"}

@app.post("/api/summarize/full", response_model=FullSummaryResponse)
async def summarize_full_article(request: FullSummaryRequest):
    """
    Generate a comprehensive summary of a full article by fetching and analyzing the full content
    
    Args:
        request: FullSummaryRequest with article URL
        
    Returns:
        FullSummaryResponse with comprehensive summary and word count
    """
    url = request.url
    
    # Check rate limit
    if not check_rate_limit():
        raise HTTPException(
            status_code=429, 
            detail="Rate limit exceeded. Maximum 10 full summaries per minute."
        )
    
    # Check cache (24 hour TTL)
    if url in full_summary_cache:
        cache_entry = full_summary_cache[url]
        cache_age = (datetime.now() - cache_entry["timestamp"]).total_seconds()
        
        if cache_age < 86400:  # 24 hours
            print(f"📦 Returning cached full summary for {url}")
            return FullSummaryResponse(
                summary=cache_entry["summary"],
                word_count=cache_entry["word_count"],
                url=url,
                cached=True
            )
        else:
            # Expired cache, remove it
            del full_summary_cache[url]
    
    print(f"🔄 Fetching full article content from {url}")
    
    try:
        # Scrape article content
        article_content = await web_scraper.extract_article_content(url)
        
        if not article_content:
            raise HTTPException(
                status_code=400,
                detail="Could not extract article content from URL. The article may be behind a paywall or the URL is invalid."
            )
        
        # Find article title from cache or use URL
        article_title = "Article"
        for cache_key in cache:
            for article in cache[cache_key]["articles"]:
                if article.url == url:
                    article_title = article.title
                    break
        
        print(f"📄 Extracted {len(article_content)} characters from article")
        print("🤖 Generating comprehensive summary...")
        
        # Generate comprehensive summary using async executor
        loop = asyncio.get_event_loop()
        summary = await loop.run_in_executor(
            None,
            ai_service.summarize_full_article,
            article_title,
            article_content
        )
        
        word_count = len(summary.split())
        
        # Cache the summary
        full_summary_cache[url] = {
            "summary": summary,
            "word_count": word_count,
            "timestamp": datetime.now()
        }
        
        print(f"✅ Successfully generated {word_count}-word summary")
        
        return FullSummaryResponse(
            summary=summary,
            word_count=word_count,
            url=url,
            cached=False
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating full summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.get("/api/news/{article_id}", response_model=Article)
async def get_article(article_id: str):
    """Get a specific article by ID from any cache"""
    # Search all cache entries
    for cache_key in cache:
        for article in cache[cache_key]["articles"]:
            if article.id == article_id:
                return article
    
    raise HTTPException(status_code=404, detail="Article not found")

# Run with: uvicorn main:app --reload

