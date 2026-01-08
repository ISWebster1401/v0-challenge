"""
News endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional
import asyncio
import os

from models.schemas import Article, NewsResponse
from core.cache import cache, get_cache_key_str, is_cache_valid, get_cache_age
from core.dependencies import get_news_service, get_ai_service

router = APIRouter()


@router.get("", response_model=NewsResponse)
async def get_news(
    limit: int = 10, 
    force_refresh: bool = False,
    from_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    to_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    topic: Optional[str] = Query(None, description="Filter by topic (e.g., AI, Hardware, Mobile)"),
    page: int = 1
):
    """
    Get latest tech news with AI summaries, optionally filtered by date range
    
    Args:
        limit: Number of articles per page (1-100)
        force_refresh: Force cache refresh
        from_date: Filter articles published on or after this date (YYYY-MM-DD string)
        to_date: Filter articles published on or before this date (YYYY-MM-DD string)
        topic: Filter by topic
        page: Page number (starts at 1)
        
    Returns:
        NewsResponse with articles and metadata
    """
    # Validate limit
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
    
    # Validate page
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be >= 1")
    
    # Validate date range (convert strings to dates for comparison)
    if from_date and to_date:
        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
            if from_dt > to_dt:
                raise HTTPException(status_code=400, detail="from_date must be before or equal to to_date")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Generate cache key based on date range and topic (use strings directly)
    cache_key = get_cache_key_str(from_date, to_date, topic)
    
    # Get services
    news_service = get_news_service()
    ai_service = get_ai_service()
    
    # Check cache
    if is_cache_valid(cache_key) and not force_refresh:
        print(f"📦 Returning cached results for key: {cache_key}")
        cache_entry = cache[cache_key]
        all_cached_articles = cache_entry["articles"]
        
        # Get cached topics if available, otherwise extract from titles
        if "topics" in cache_entry and cache_entry["topics"]:
            topics = cache_entry["topics"]
        else:
            # Extract topics from cached article titles using AI
            cached_titles = [article.title for article in all_cached_articles]
            if cached_titles:
                loop = asyncio.get_event_loop()
                topics = await loop.run_in_executor(
                    None,
                    ai_service.extract_topics_from_titles,
                    cached_titles
                )
                # Cache topics for future use
                cache_entry["topics"] = topics
            else:
                topics = []
        
        # Pagination
        total_articles = len(all_cached_articles)
        total_pages = (total_articles + limit - 1) // limit if total_articles > 0 else 1
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_articles = all_cached_articles[start_idx:end_idx]
        
        return NewsResponse(
            articles=paginated_articles,
            count=len(paginated_articles),
            cached=True,
            cache_age=get_cache_age(cache_key),
            topics=topics,
            total_pages=total_pages,
            current_page=page
        )
    
    date_range_str = f" from {from_date} to {to_date}" if from_date or to_date else ""
    topic_str = f" (topic: {topic})" if topic else ""
    print(f"🔄 Fetching fresh news{date_range_str}{topic_str}...")
    print(f"🔍 Request params: limit={limit}, from_date={from_date}, to_date={to_date}, topic={topic}, page={page}")
    
    try:
        # For date ranges, fetch more articles to allow pagination
        # Fetch up to 100 articles (NewsAPI max) when date filtering is active
        fetch_limit = 100 if (from_date or to_date) else limit
        # Fetch news from NewsAPI with date filtering and topic (dates are already strings)
        articles = await news_service.fetch_top_tech_news(limit=fetch_limit, from_date=from_date, to_date=to_date, topic=topic)
        print(f"📦 Received {len(articles)} articles from news_service")
        
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for the specified date range")
        
        print(f"📰 Fetched {len(articles)} articles")
        
        # Extract topics from titles BEFORE summarization (saves API costs)
        article_titles = [article["title"] for article in articles]
        print("🤖 Extracting topics from titles...")
        loop = asyncio.get_event_loop()
        topics = await loop.run_in_executor(
            None,
            ai_service.extract_topics_from_titles,
            article_titles
        )
        print(f"📊 Extracted {len(topics)} trending topics: {', '.join(topics)}")
        
        print("🤖 Generating AI summaries...")
        # Generate AI summaries
        summarized_articles = await ai_service.summarize_articles_batch(articles)
        
        # Update cache for this date range
        cache[cache_key]["articles"] = [Article(**article) for article in summarized_articles]
        cache[cache_key]["topics"] = topics  # Cache topics with articles
        cache[cache_key]["timestamp"] = datetime.now()
        cache[cache_key]["ttl"] = int(os.getenv("CACHE_TTL", 900))
        
        # Pagination
        all_articles = cache[cache_key]["articles"]
        total_articles = len(all_articles)
        total_pages = (total_articles + limit - 1) // limit if total_articles > 0 else 1
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_articles = all_articles[start_idx:end_idx]
        
        print(f"✅ Successfully processed {len(summarized_articles)} articles")
        
        return NewsResponse(
            articles=paginated_articles,
            count=len(paginated_articles),
            cached=False,
            cache_age=0,
            topics=topics,
            total_pages=total_pages,
            current_page=page
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.post("/refresh")
async def refresh_cache(
    from_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    to_date: Optional[str] = Query(None, regex=r"^\d{4}-\d{2}-\d{2}$"),
    topic: Optional[str] = Query(None, description="Filter by topic")
):
    """Force refresh the news cache for a specific date range and topic"""
    cache_key = get_cache_key_str(from_date, to_date, topic)
    cache[cache_key]["articles"] = []
    cache[cache_key]["timestamp"] = None
    return {"message": f"Cache cleared for date range: {cache_key}", "status": "success"}


@router.get("/{article_id}", response_model=Article)
async def get_article(article_id: str):
    """Get a specific article by ID from any cache"""
    # Search all cache entries
    for cache_key in cache:
        for article in cache[cache_key]["articles"]:
            if article.id == article_id:
                return article
    
    raise HTTPException(status_code=404, detail="Article not found")
