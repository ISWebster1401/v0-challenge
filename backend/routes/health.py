"""
Health check endpoints
"""
from fastapi import APIRouter
from models.schemas import HealthResponse
from core.cache import cache

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    total_articles = sum(len(cache[key]["articles"]) for key in cache)
    return HealthResponse(
        status="healthy",
        cache_size=total_articles,
        cache_age_seconds=None  # Multiple caches, can't provide single age
    )
