"""
Tech News Summarizer API - Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routes import news, health, summarize

# Load environment variables
load_dotenv()

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

# Root endpoint
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

# Register routers
app.include_router(health.router, tags=["health"])
app.include_router(news.router, prefix="/api/news", tags=["news"])
app.include_router(summarize.router, prefix="/api/summarize", tags=["summarize"])

# Run with: uvicorn main:app --reload
