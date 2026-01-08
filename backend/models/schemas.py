from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class Article(BaseModel):
    id: str
    title: str
    summary: str
    url: str
    source: str
    publishedAt: datetime
    imageUrl: Optional[str] = None
    description: Optional[str] = None

class NewsResponse(BaseModel):
    articles: list[Article]
    count: int
    cached: bool
    cache_age: Optional[int] = None
    topics: list[str] = []
    total_pages: int = 1
    current_page: int = 1

class HealthResponse(BaseModel):
    status: str
    cache_size: int
    cache_age_seconds: Optional[int] = None

class FullSummaryRequest(BaseModel):
    url: str

class FullSummaryResponse(BaseModel):
    summary: str
    word_count: int
    url: str
    cached: bool = False

class ExplainRequest(BaseModel):
    selected_text: str
    context: Optional[str] = None

class ExplainResponse(BaseModel):
    explanation: str
