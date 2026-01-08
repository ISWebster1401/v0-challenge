"""
Tech News Summarizer API - Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables FIRST, before importing routes
load_dotenv()

from routes import news, health, summarize

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
# Get allowed origins from environment or use defaults
allowed_origins_env = os.getenv(
    "ALLOWED_ORIGINS",
    "https://v0-challenge-five.vercel.app,http://localhost:5173,http://localhost:3000"
)

# Split and clean origins
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

# For production, add regex pattern to allow all Vercel subdomains
allow_origin_regex = None
if os.getenv("ENVIRONMENT") == "production":
    # Allow all *.vercel.app subdomains
    allow_origin_regex = r"https://.*\.vercel\.app"

print(f"🌐 CORS allowed origins: {allowed_origins}")
if allow_origin_regex:
    print(f"🌐 CORS origin regex: {allow_origin_regex}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
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
