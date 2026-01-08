# Backend - Tech News Summarizer API

FastAPI backend that provides AI-powered news summarization, topic extraction, and article analysis.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Architecture](#architecture)
- [Deployment](#deployment)

## ✨ Features

- **AI Summarization**: Generate concise summaries using GPT-4o-mini
- **Full Article Summaries**: Comprehensive summaries using GPT-4o
- **Text Explanation**: Explain selected text using GPT-4o
- **News Fetching**: Fetch tech news from NewsAPI with intelligent filtering
- **Topic Extraction**: AI-powered topic extraction from article titles
- **Smart Caching**: In-memory caching with configurable TTL
- **Rate Limiting**: Protect expensive endpoints
- **Day-by-Day Fetching**: Ensures complete coverage for date ranges
- **Deduplication**: Removes duplicate articles intelligently

## 🛠 Tech Stack

- **FastAPI 0.109.0**: Web framework
- **Python 3.9+**: Programming language
- **OpenAI 1.10.0**: AI models (GPT-4o, GPT-4o-mini)
- **HTTPX 0.26.0**: Async HTTP client
- **BeautifulSoup4 4.12.2**: Web scraping
- **Pydantic 2.5.3**: Data validation
- **Uvicorn**: ASGI server
- **Python-dotenv**: Environment variable management

## 📁 Project Structure

```
backend/
├── core/
│   ├── __init__.py
│   ├── cache.py          # Cache management utilities
│   ├── dependencies.py   # Service dependency injection
│   └── rate_limit.py    # Rate limiting utilities
│
├── models/
│   ├── __init__.py
│   └── schemas.py        # Pydantic models
│
├── routes/
│   ├── __init__.py
│   ├── health.py         # Health check endpoint
│   ├── news.py           # News endpoints
│   └── summarize.py      # Summarization endpoints
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py     # OpenAI integration
│   ├── news_service.py   # NewsAPI integration
│   └── web_scraper.py    # Web scraping utilities
│
├── main.py               # FastAPI app entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## 🚀 Installation

### 1. Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### 2. Create Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

Required environment variables:
```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
CACHE_TTL=900
ENVIRONMENT=development
```

### 5. Get API Keys

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy and paste into `.env`

**NewsAPI Key:**
1. Go to https://newsapi.org/register
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy and paste into `.env`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | - | ✅ Yes |
| `NEWS_API_KEY` | NewsAPI key for fetching news | - | ✅ Yes |
| `CACHE_TTL` | Cache time-to-live in seconds | 900 | ❌ No |
| `ENVIRONMENT` | Environment (development/production) | development | ❌ No |

### Cache Configuration

- **Article Cache**: 15 minutes (900 seconds) - configurable via `CACHE_TTL`
- **Full Summary Cache**: 24 hours (86400 seconds) - hardcoded
- **Cache Keys**: Based on date range and topic for proper isolation

### Rate Limiting

- **Full Summary Endpoint**: 10 requests per minute
- **Explain Endpoint**: 10 requests per minute
- Uses sliding window algorithm

## 🏃 Running the Server

### Development Mode

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Different Ports

```bash
uvicorn main:app --reload --port 8080
```

### Access Points

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📡 API Endpoints

### News Endpoints

#### `GET /api/news`
Get latest tech news with AI summaries.

**Query Parameters:**
- `limit` (int, 1-100, default: 10)
- `page` (int, default: 1)
- `from_date` (string, YYYY-MM-DD, optional)
- `to_date` (string, YYYY-MM-DD, optional)
- `topic` (string, optional)
- `force_refresh` (bool, default: false)

**Response:**
```json
{
  "articles": [...],
  "count": 10,
  "cached": false,
  "cache_age": 0,
  "topics": ["AI", "Hardware", "Mobile"],
  "total_pages": 5,
  "current_page": 1
}
```

#### `POST /api/news/refresh`
Force refresh cache for a date range.

#### `GET /api/news/{article_id}`
Get specific article by ID.

### Summarization Endpoints

#### `POST /api/summarize/full`
Generate comprehensive summary of full article.

**Request:**
```json
{
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "summary": "Comprehensive summary...",
  "word_count": 250,
  "url": "https://example.com/article",
  "cached": false
}
```

#### `POST /api/summarize/explain`
Explain selected text in detail.

**Request:**
```json
{
  "selected_text": "Text to explain",
  "context": "Optional context"
}
```

**Response:**
```json
{
  "explanation": "Detailed explanation..."
}
```

### Health Endpoint

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "cache_size": 150,
  "cache_age_seconds": null
}
```

## 🏗 Architecture

### Service Layer

- **AIService**: Handles all OpenAI interactions
  - `summarize_article()`: Quick summaries (GPT-4o-mini)
  - `summarize_full_article()`: Comprehensive summaries (GPT-4o)
  - `explain_better()`: Text explanations (GPT-4o)
  - `extract_topics_from_titles()`: Topic extraction (GPT-4o-mini)

- **NewsService**: Handles NewsAPI interactions
  - `fetch_top_tech_news()`: Fetch and filter news
  - `_fetch_articles_by_day()`: Day-by-day fetching
  - `_sample_articles_intelligently()`: Smart article distribution
  - `_score_articles()`: Article quality scoring

- **WebScraper**: Extracts full article content
  - `extract_article_content()`: Scrapes article text

### Routing Layer

- **Modular Structure**: Each feature has its own router
- **Dependency Injection**: Services initialized lazily
- **Error Handling**: Comprehensive error handling with clear messages

### Caching Strategy

- **Article Cache**: Keyed by date range + topic
- **Full Summary Cache**: Keyed by article URL
- **TTL-based Expiration**: Automatic cache invalidation

## 🚢 Deployment

### Railway Deployment

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment Variables**
   - Go to Variables tab
   - Add:
     - `OPENAI_API_KEY`
     - `NEWS_API_KEY`
     - `CACHE_TTL` (optional)
     - `ENVIRONMENT=production`

4. **Set Start Command**
   - Go to Settings → Deploy
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Deploy**
   - Railway will auto-detect Python
   - It will install dependencies from `requirements.txt`
   - Your API will be live at `https://your-app.railway.app`

### Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t tech-news-api .
docker run -p 8000:8000 --env-file .env tech-news-api
```

## 🐛 Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**2. OpenAI API Key Error**
```
Error: The api_key client option must be set
```
- Check `.env` file exists
- Verify `OPENAI_API_KEY` is set correctly
- Restart the server after changing `.env`

**3. NewsAPI Rate Limit**
- Free tier: 100 requests/day
- Consider upgrading or implementing request queuing

**4. Port Already in Use**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --port 8080
```

**5. Import Errors After Refactoring**
- Ensure `load_dotenv()` is called before importing routes
- Check all imports use relative paths correctly

## 📊 Performance

### Optimization Tips

1. **Caching**: Articles cached for 15 minutes reduces API calls
2. **Parallel Processing**: Article summaries generated in parallel
3. **Lazy Loading**: Services initialized only when needed
4. **Smart Sampling**: Fetches more articles but selects best ones

### Monitoring

- Check `/health` endpoint for cache statistics
- Monitor OpenAI API usage in OpenAI dashboard
- Track NewsAPI usage in NewsAPI dashboard

## 🔒 Security

- **API Keys**: Never commit `.env` file to git
- **CORS**: Configured for production (update `allow_origins` in `main.py`)
- **Rate Limiting**: Prevents abuse of expensive endpoints
- **Input Validation**: Pydantic models validate all inputs

## 📝 Development Tips

1. **Use Interactive Docs**: Visit `/docs` for easy API testing
2. **Check Logs**: Server logs show detailed request/response info
3. **Test Locally**: Always test changes locally before deploying
4. **Environment Variables**: Use `.env.example` as template

## 🤝 Contributing

When adding new features:

1. Follow existing code structure
2. Add routes in `routes/` directory
3. Add services in `services/` directory
4. Update schemas in `models/schemas.py`
5. Add error handling
6. Update this README if needed

---

**Happy Coding! 🚀**
