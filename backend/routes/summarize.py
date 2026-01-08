"""
Full article summarization endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import asyncio

from models.schemas import FullSummaryRequest, FullSummaryResponse, ExplainRequest, ExplainResponse
from core.cache import cache, full_summary_cache
from core.rate_limit import check_rate_limit
from core.dependencies import get_ai_service, get_web_scraper

router = APIRouter()


@router.post("/full", response_model=FullSummaryResponse)
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
    
    # Get services
    ai_service = get_ai_service()
    web_scraper = get_web_scraper()
    
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


@router.post("/explain", response_model=ExplainResponse)
async def explain_text(request: ExplainRequest):
    """
    Provide a detailed explanation of selected text
    
    Args:
        request: ExplainRequest with selected text and optional context
        
    Returns:
        ExplainResponse with detailed explanation
    """
    # Check rate limit
    if not check_rate_limit():
        raise HTTPException(
            status_code=429, 
            detail="Rate limit exceeded. Maximum 10 requests per minute."
        )
    
    if not request.selected_text or len(request.selected_text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Selected text must be at least 10 characters long."
        )
    
    print(f"🤖 Explaining selected text: {request.selected_text[:100]}...")
    
    # Get AI service
    ai_service = get_ai_service()
    
    try:
        # Generate explanation using async executor
        loop = asyncio.get_event_loop()
        explanation = await loop.run_in_executor(
            None,
            ai_service.explain_better,
            request.selected_text,
            request.context or ""
        )
        
        print(f"✅ Successfully generated explanation")
        
        return ExplainResponse(explanation=explanation)
        
    except Exception as e:
        print(f"❌ Error generating explanation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")
