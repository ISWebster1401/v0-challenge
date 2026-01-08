# 🚀 Tech News Summarizer

A modern, AI-powered web application that fetches the latest tech news and generates intelligent summaries using OpenAI GPT-4o. Built with FastAPI (backend) and React + Vite (frontend).

![Tech News Summarizer](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18+-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
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

## 🚀 Quick Start

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

See [backend/README.md](./backend/README.md) for detailed instructions.

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
uvicorn main:app --reload
```

### 3. Frontend Setup

See [frontend/README.md](./frontend/README.md) for detailed instructions.

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your backend URL
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ⚙️ Configuration

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_newsapi_key_here
CACHE_TTL=900
ENVIRONMENT=development
```

### Frontend Environment Variables

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000
```

For production, set `VITE_API_URL` to your deployed backend URL.

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

### Backend (Railway)

1. Push your code to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repository
4. Add environment variables in Railway dashboard:
   - `OPENAI_API_KEY`
   - `NEWS_API_KEY`
   - `CACHE_TTL` (optional)
5. Railway will auto-detect Python and install dependencies
6. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

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

## 🙏 Acknowledgments

- OpenAI for GPT-4o and GPT-4o-mini
- NewsAPI for news aggregation
- FastAPI and React communities
- V0 for the challenge inspiration

---

**Made with ❤️ using AI**
