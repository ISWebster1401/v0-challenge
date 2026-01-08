"""
Dependency injection for services
"""
import os
from services.news_service import NewsService
from services.ai_service import AIService
from services.web_scraper import WebScraper

# Lazy initialization - services are created when first accessed
_news_service = None
_ai_service = None
_web_scraper = None


def get_news_service() -> NewsService:
    """Get or create NewsService instance"""
    global _news_service
    if _news_service is None:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            raise ValueError("NEWS_API_KEY environment variable is not set")
        _news_service = NewsService(api_key=api_key)
    return _news_service


def get_ai_service() -> AIService:
    """Get or create AIService instance"""
    global _ai_service
    if _ai_service is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _ai_service = AIService(api_key=api_key)
    return _ai_service


def get_web_scraper() -> WebScraper:
    """Get or create WebScraper instance"""
    global _web_scraper
    if _web_scraper is None:
        _web_scraper = WebScraper()
    return _web_scraper
