# 🚀 Tech News Summarizer

> **🌐 Live Demo:** https://v0-challenge-one.vercel.app
> **📡 API Docs:** https://v0-challenge-production.up.railway.app/docs


A modern, AI-powered web application that fetches the latest tech news and generates intelligent summaries using OpenAI GPT-4o. Built with FastAPI (backend) and React + Vite (frontend).

![Tech News Summarizer](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start / How to Run Locally](#-quick-start--how-to-run-locally)
- [Configuration / Setup & API Keys](#-configuration--setup--api-keys)
- [AI Tools Used and How They Were Used](#-ai-tools-used-and-how-they-were-used)
- [Approach and Tradeoffs](#-approach-and-tradeoffs)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [What I'd Build Next](#-what-id-build-next-with-more-time)
- [Assumptions Made](#-assumptions-made)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### Core Features
- **AI-Powered Summaries**: Generate concise summaries using OpenAI GPT-4o-mini for quick overviews
- **Comprehensive Full Summaries**: Get detailed 8-12 sentence summaries using GPT-4o for in-depth analysis
- **Smart Text Explanation**: Select any text in a summary and get a detailed explanation using GPT-4o
- **Date Range Filtering**: Filter news by date ranges (Today, Yesterday, Last 7 Days, Custom)
- **Trending Topics**: AI-extracted trending topics with one-click filtering
- **Real-time Search**: Search across article titles, summaries, and sources
- **Dark Mode**: Beautiful dark/light theme with persistent preferences
- **Pagination**: Navigate through articles efficiently
- **Intelligent Article Sampling**: Prioritizes important news and distributes evenly across date ranges

### Advanced Features
- **Day-by-Day Fetching**: For date ranges ≥5 days, fetches articles day-by-day to ensure complete coverage
- **Deduplication**: Removes duplicate articles by URL and similar titles
- **Smart Caching**: In-memory caching with configurable TTL (15 min for articles, 24h for full summaries)
- **Rate Limiting**: Protects full summary endpoint (10 requests/minute)
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Programming language
- **OpenAI GPT-4o/GPT-4o-mini**: AI models for summarization and topic extraction
- **NewsAPI**: Tech news aggregation
- **BeautifulSoup4**: Web scraping for full article content
- **HTTPX**: Async HTTP client
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Hooks**: State management

## 📁 Project Structure

```
v0-challenge/
├── backend/
│   ├── core/              # Core utilities (cache, rate limiting, dependencies)
│   ├── models/            # Pydantic schemas
│   ├── routes/            # API endpoints (news, health, summarize)
│   ├── services/          # Business logic (AI, news, web scraping)
│   ├── main.py           # FastAPI app entry point
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # Backend-specific documentation
│
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API client
│   │   └── App.jsx       # Main app component
│   ├── package.json      # Node dependencies
│   └── README.md         # Frontend-specific documentation
│
└── README.md            # This file
```

## 🚀 Quick Start / How to Run Locally

### Prerequisites

- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **NewsAPI Key** ([Get one here](https://newsapi.org/register))

### 1. Clone the Repository

```bash
git clone <repository-url>
cd v0-challenge
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys (see Configuration section below)
uvicorn main:app --reload
```

The backend will run on **http://localhost:8000**

### 3. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your backend URL (default: http://localhost:8000)
npm run dev
```

The frontend will run on **http://localhost:5173**

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

For more detailed setup instructions, see:
- [backend/README.md](./backend/README.md)
- [frontend/README.md](./frontend/README.md)

## ⚙️ Configuration / Setup & API Keys

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
CACHE_TTL=900
ENVIRONMENT=development
```

**Important**: Never commit the `.env` file to git. Use `.env.example` as a template.

**How to get API keys:**
- **OpenAI API Key**: Sign up at https://platform.openai.com/api-keys and create a new key
- **NewsAPI Key**: Register at https://newsapi.org/register (free tier: 100 requests/day)

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

For production, set `VITE_API_URL` to your deployed backend URL (e.g., `https://your-backend.railway.app`).

## 🤖 AI Tools Used and How They Were Used

This project extensively uses **OpenAI's GPT models** for intelligent content processing:

### 1. **GPT-4o-mini** - Quick Article Summaries
- **Purpose**: Generate concise 2-3 sentence summaries for article cards
- **Usage**: Called via `AIService.summarize_article()` for each article in the feed
- **Why**: Fast, cost-effective for bulk processing, maintains good quality
- **Implementation**: Processes article title + description, returns brief summary
- **Location**: `backend/services/ai_service.py` → `summarize_article()`

### 2. **GPT-4o-mini** - Topic Extraction
- **Purpose**: Extract 5-8 trending topics from article titles
- **Usage**: Called via `AIService.extract_topics_from_titles()` after fetching articles
- **Why**: More accurate than keyword matching, understands context and themes
- **Implementation**: Analyzes all article titles, returns JSON array of topics
- **Location**: `backend/services/ai_service.py` → `extract_topics_from_titles()`

### 3. **GPT-4o** - Comprehensive Full Summaries
- **Purpose**: Generate detailed 8-12 sentence summaries of full article content
- **Usage**: Called via `AIService.summarize_full_article()` when user clicks "Full Summary"
- **Why**: More powerful model for in-depth analysis, better context understanding
- **Implementation**: Processes full scraped article content (up to 6000 chars), returns comprehensive summary
- **Location**: `backend/services/ai_service.py` → `summarize_full_article()`

### 4. **GPT-4o** - Text Explanation ("Explain Better")
- **Purpose**: Provide detailed explanations of selected text from summaries
- **Usage**: Called via `AIService.explain_better()` when user selects text and clicks "Explain Better"
- **Why**: Helps users understand complex concepts, provides context and implications
- **Implementation**: Takes selected text + article context, returns educational explanation
- **Location**: `backend/services/ai_service.py` → `explain_better()`

### AI Integration Approach

- **Lazy Initialization**: AI services are only created when needed (saves resources)
- **Async Processing**: Article summaries generated in parallel for better performance
- **Caching**: Full summaries cached for 24 hours to reduce API costs
- **Rate Limiting**: Full summary endpoint limited to 10 requests/minute
- **Error Handling**: Graceful fallbacks if AI service fails
- **Cost Optimization**: Uses GPT-4o-mini for bulk operations, GPT-4o only for premium features

### AI Model Selection Rationale

- **GPT-4o-mini for summaries**: Fast, cost-effective, sufficient quality for quick overviews
- **GPT-4o for full summaries**: Better understanding of complex articles, more detailed analysis
- **GPT-4o for explanations**: Superior reasoning for educational content

## 💡 Approach and Tradeoffs

### Architecture Decisions

**Monorepo Structure**
- ✅ **Pros**: Single repository, easier to manage, shared configurations
- ❌ **Cons**: Larger repo size, but acceptable for this project size

**FastAPI Backend**
- ✅ **Pros**: Modern async framework, automatic API docs, type safety with Pydantic
- ❌ **Cons**: Python can be slower than Go/Rust, but sufficient for this use case

**React + Vite Frontend**
- ✅ **Pros**: Fast development, great DX, modern tooling, excellent performance
- ❌ **Cons**: Larger bundle size than vanilla JS, but Vite optimizes well

**In-Memory Caching**
- ✅ **Pros**: Fast, simple, no external dependencies
- ❌ **Cons**: Lost on restart, not shared across instances (acceptable for current scale)

**Day-by-Day Fetching for Date Ranges**
- ✅ **Pros**: Ensures complete coverage, distributes articles evenly
- ❌ **Cons**: More API calls to NewsAPI (but necessary for quality)

### Tradeoffs Made

1. **Caching Strategy**: Chose in-memory over Redis for simplicity, acceptable for single-instance deployment
2. **AI Model Selection**: GPT-4o-mini for bulk, GPT-4o for premium features balances cost and quality
3. **Client-side Filtering**: Search and topic filtering done client-side for instant feedback, acceptable for <100 articles
4. **No Database**: Articles cached in memory, acceptable since NewsAPI is the source of truth
5. **Rate Limiting**: Simple deque-based rate limiting, sufficient for current scale

## 📚 API Documentation

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: Your deployed backend URL

### Endpoints

#### `GET /api/news`
Get latest tech news with AI summaries.

**Query Parameters:**
- `limit` (int, default: 10): Number of articles per page (1-100)
- `page` (int, default: 1): Page number
- `from_date` (string, optional): Filter from date (YYYY-MM-DD)
- `to_date` (string, optional): Filter to date (YYYY-MM-DD)
- `topic` (string, optional): Filter by topic (e.g., "AI", "Hardware")
- `force_refresh` (bool, default: false): Force cache refresh

**Example:**
```bash
GET /api/news?limit=10&from_date=2026-01-01&to_date=2026-01-07&topic=AI
```

#### `POST /api/news/refresh`
Force refresh the cache for a specific date range.

**Query Parameters:**
- `from_date` (string, optional)
- `to_date` (string, optional)
- `topic` (string, optional)

#### `POST /api/summarize/full`
Generate a comprehensive summary of a full article.

**Request Body:**
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

**Request Body:**
```json
{
  "selected_text": "Text to explain",
  "context": "Optional context from article"
}
```

**Response:**
```json
{
  "explanation": "Detailed explanation..."
}
```

#### `GET /health`
Health check endpoint.

#### `GET /api/news/{article_id}`
Get a specific article by ID.

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 🚢 Deployment

### Deployed Links

- **Frontend (Production)**: https://v0-challenge-five.vercel.app
- **Backend API (Production)**: https://v0-challenge-production.up.railway.app
- **API Documentation**: https://v0-challenge-production.up.railway.app/docs

### Backend (Railway)

1. Push your code to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Add environment variables in Railway dashboard:
   - `OPENAI_API_KEY`
   - `NEWS_API_KEY`
   - `ENVIRONMENT=production`
   - `CACHE_TTL=900` (optional)
5. Railway will auto-detect Python and install dependencies
6. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

See [backend/RAILWAY_SETUP.md](./backend/RAILWAY_SETUP.md) for detailed Railway setup instructions.

### Frontend (Vercel)

1. Push your code to GitHub
2. Import project on [Vercel](https://vercel.com)
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable:
   - `VITE_API_URL`: Your Railway backend URL
6. Deploy!

### Environment Variables for Production

**Backend (Railway):**
```env
OPENAI_API_KEY=your_key
NEWS_API_KEY=your_key
CACHE_TTL=900
ENVIRONMENT=production
```

**Frontend (Vercel):**
```env
VITE_API_URL=https://your-backend.railway.app
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
source venv/bin/activate
pytest  # If tests are added
```

### Frontend Testing

```bash
cd frontend
npm test  # If tests are added
```

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError`
- **Solution**: Ensure virtual environment is activated and dependencies are installed

**Issue**: `OPENAI_API_KEY not set`
- **Solution**: Check `.env` file exists and contains valid API key

**Issue**: Rate limit errors
- **Solution**: Full summary endpoint is limited to 10 requests/minute

### Frontend Issues

**Issue**: Cannot connect to backend
- **Solution**: Check `VITE_API_URL` in `.env` matches your backend URL

**Issue**: CORS errors
- **Solution**: Ensure backend CORS middleware allows your frontend origin

## 📝 Development

### Adding New Features

1. **Backend**: Add routes in `backend/routes/`, services in `backend/services/`
2. **Frontend**: Add components in `frontend/src/components/`
3. Follow existing code patterns and structure

### Code Style

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Use ESLint and Prettier (if configured)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is built for the V0 Challenge. All rights reserved.

## 👤 Author

**Sebastian Webster**
- Built for V0 Challenge
- 2026

## 🔮 What I'd Build Next (With More Time)

### Short-term Improvements (1-2 weeks)

1. **User Authentication & Personalization**
   - User accounts with saved preferences
   - Personalized news feed based on reading history
   - Bookmark favorite articles
   - Reading history tracking

2. **Enhanced Search & Filtering**
   - Advanced search with filters (date, source, topic combinations)
   - Saved search queries
   - Search suggestions/autocomplete
   - Full-text search across article content

3. **Better Caching & Performance**
   - Redis for distributed caching
   - CDN for static assets
   - Database for article storage (PostgreSQL)
   - Background job processing for article fetching

4. **Notifications & Alerts**
   - Email digests (daily/weekly summaries)
   - Browser notifications for breaking news
   - Topic-based alerts
   - RSS feed support

### Medium-term Features (1-2 months)

5. **Social Features**
   - Share articles with comments
   - Community discussions
   - User ratings/reviews
   - Collaborative filtering ("Users who read this also read...")

6. **Advanced AI Features**
   - Personalized summary length preferences
   - Multi-language support with translation
   - Sentiment analysis
   - Article recommendations based on AI understanding
   - Automated fact-checking integration

7. **Analytics Dashboard**
   - Reading statistics
   - Topic trends over time
   - Source credibility scores
   - Personal reading insights

8. **Mobile App**
   - Native iOS/Android apps
   - Offline reading support
   - Push notifications
   - Better mobile UX

### Long-term Vision (3-6 months)

9. **Content Aggregation Platform**
   - Multiple news sources beyond NewsAPI
   - User-submitted articles
   - Community moderation
   - Editorial team for curated content

10. **AI-Powered Research Assistant**
    - Deep dive research on topics
    - Cross-article analysis
    - Timeline generation
    - Impact assessment

11. **Enterprise Features**
    - Team workspaces
    - Custom news feeds for organizations
    - API access for developers
    - White-label solutions

12. **Advanced Personalization**
    - Machine learning models for content recommendation
    - Adaptive UI based on usage patterns
    - Smart notifications
    - Learning from user feedback

### Technical Improvements

- **Testing**: Comprehensive test suite (unit, integration, e2e)
- **Monitoring**: APM, error tracking (Sentry), logging (Datadog)
- **CI/CD**: Automated testing and deployment pipelines
- **Documentation**: API versioning, OpenAPI specs, SDKs
- **Scalability**: Horizontal scaling, load balancing, microservices architecture
- **Security**: Rate limiting per user, API authentication, data encryption

## 🙏 Acknowledgments

- **OpenAI** for GPT-4o and GPT-4o-mini - Powering all AI features
- **NewsAPI** for news aggregation
- **FastAPI** and **React** communities for excellent frameworks
- **V0** for the challenge inspiration

## 📝 Assumptions Made

1. **NewsAPI Free Tier**: Assumed 100 requests/day is sufficient for initial deployment
2. **Single Instance**: Designed for single-instance deployment initially (can scale later)
3. **English Only**: Focused on English-language tech news (can expand later)
4. **Tech News Focus**: Specialized for technology news (can generalize later)
5. **No User Accounts**: Built as public-facing app initially (auth can be added)

---

**Made with ❤️ using AI**
