# Frontend - Tech News Summarizer

Modern React application with Vite for browsing and reading AI-powered tech news summaries.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [Building for Production](#building-for-production)
- [Deployment](#deployment)
- [Components](#components)

## ✨ Features

- **AI-Powered Summaries**: View concise and comprehensive article summaries
- **Text Selection & Explanation**: Select text to get detailed explanations
- **Date Filtering**: Filter news by date ranges (Today, Yesterday, Last 7 Days, Custom)
- **Trending Topics**: Click topics to filter articles
- **Real-time Search**: Search across titles, summaries, and sources
- **Dark Mode**: Beautiful dark/light theme with localStorage persistence
- **Pagination**: Navigate through articles efficiently
- **Responsive Design**: Works on all screen sizes
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages

## 🛠 Tech Stack

- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls
- **React Hooks**: State management

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── DateFilter.jsx        # Date range filtering
│   │   ├── FullSummaryModal.jsx  # Full summary modal with text selection
│   │   ├── Header.jsx             # App header with search and topics
│   │   ├── HighlightText.jsx     # Text highlighting for search
│   │   ├── LoadingSpinner.jsx    # Loading indicator
│   │   ├── NewsCard.jsx          # Individual article card
│   │   ├── NewsList.jsx          # Article grid/list
│   │   ├── Pagination.jsx        # Page navigation
│   │   ├── SearchBar.jsx         # Search input
│   │   └── TrendingTopics.jsx    # Topic tags
│   │
│   ├── hooks/
│   │   └── useDarkMode.js       # Dark mode hook
│   │
│   ├── services/
│   │   └── api.js                # API client
│   │
│   ├── App.jsx                   # Main app component
│   ├── main.jsx                  # React entry point
│   └── index.css                 # Global styles
│
├── index.html                    # HTML template
├── package.json                  # Dependencies
├── tailwind.config.js            # Tailwind configuration
├── vite.config.js               # Vite configuration
├── vercel.json                  # Vercel deployment config
└── README.md                    # This file
```

## 🚀 Installation

### 1. Prerequisites

- **Node.js 18+** installed
- **npm** or **yarn** package manager

### 2. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 3. Set Up Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

Set your backend API URL:
```env
VITE_API_URL=http://localhost:8000
```

For production, use your deployed backend URL:
```env
VITE_API_URL=https://your-backend.railway.app
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_API_URL` | Backend API URL | http://localhost:8000 | ✅ Yes |

### Tailwind CSS

Tailwind is configured in `tailwind.config.js`:
- Dark mode: Class-based (`dark:` prefix)
- Content paths: All JSX/TSX files in `src/`

### Vite Configuration

Vite config in `vite.config.js`:
- React plugin enabled
- Port: 5173 (default)
- Auto-reload on file changes

## 🏃 Running the App

### Development Mode

```bash
# Start dev server
npm run dev
```

The app will be available at:
- **Local**: http://localhost:5173
- **Network**: Check terminal for network URL

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Other Commands

```bash
# Lint code (if ESLint configured)
npm run lint

# Format code (if Prettier configured)
npm run format
```

## 🏗 Building for Production

### Build Process

```bash
npm run build
```

This will:
1. Optimize and bundle all code
2. Minify JavaScript and CSS
3. Generate production-ready files in `dist/` directory
4. Create source maps for debugging

### Build Output

```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── ...
```

### Environment Variables in Production

Make sure `VITE_API_URL` is set in your deployment platform:
- **Vercel**: Add in project settings → Environment Variables
- **Netlify**: Add in site settings → Environment variables
- **Other**: Set according to platform documentation

## 🚢 Deployment

### Vercel Deployment (Recommended)

1. **Install Vercel CLI** (optional)
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   # From frontend directory
   vercel
   ```
   
   Or connect GitHub repository:
   - Go to https://vercel.com
   - Import your GitHub repository
   - Vercel will auto-detect Vite

3. **Configure**
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

4. **Environment Variables**
   - Add `VITE_API_URL` in Vercel dashboard
   - Set to your backend URL (e.g., Railway URL)

5. **Deploy**
   - Push to main branch for auto-deploy
   - Or manually deploy from dashboard

### Netlify Deployment

1. **Install Netlify CLI**
   ```bash
   npm i -g netlify-cli
   ```

2. **Deploy**
   ```bash
   netlify deploy --prod
   ```

3. **Configure in Netlify Dashboard**
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Add `VITE_API_URL` environment variable

### Other Platforms

Any static hosting service works:
- **GitHub Pages**: Use GitHub Actions to build and deploy
- **AWS S3 + CloudFront**: Upload `dist/` folder
- **Firebase Hosting**: Use Firebase CLI

## 🧩 Components

### App.jsx
Main application component that:
- Manages global state (articles, filters, pagination)
- Handles API calls
- Coordinates components

### Header.jsx
App header with:
- Title and subtitle
- Dark mode toggle
- Refresh button
- Search bar
- Trending topics
- Date filter

### NewsList.jsx
Displays articles in a responsive grid:
- Shows filtered articles
- Handles empty states
- Responsive layout (1-3 columns)

### NewsCard.jsx
Individual article card:
- Article image
- Title and summary
- Source and date
- "Full Summary" button
- "Read full article" link

### FullSummaryModal.jsx
Modal for comprehensive summaries:
- Full article summary
- Text selection functionality
- "Explain Better" button
- Detailed explanations
- Word count display

### DateFilter.jsx
Date range filtering:
- Quick filters (Today, Yesterday, Last 7 Days)
- Custom date range picker
- Chile timezone support (UTC-3)

### TrendingTopics.jsx
Topic filtering:
- Clickable topic tags
- Active state indication
- Clear topic button

### SearchBar.jsx
Real-time search:
- Debounced input (300ms)
- Result counter
- Clear button

### Pagination.jsx
Page navigation:
- Previous/Next buttons
- Page numbers
- Ellipsis for many pages
- Disabled states

## 🎨 Styling

### Tailwind CSS

The app uses Tailwind CSS for styling:
- Utility classes for rapid development
- Dark mode support via `dark:` prefix
- Responsive design with breakpoints
- Custom colors and spacing

### Dark Mode

Dark mode is implemented using:
- `useDarkMode` hook for state management
- `localStorage` for persistence
- System preference detection
- Smooth transitions

### Custom Styles

Global styles in `index.css`:
- Tailwind directives
- Base styles
- Dark mode base configuration

## 🔧 Development Tips

### Hot Module Replacement (HMR)

Vite provides instant HMR:
- Changes reflect immediately
- State is preserved when possible
- Fast refresh for React components

### Debugging

1. **React DevTools**: Install browser extension
2. **Console Logs**: Use `console.log()` for debugging
3. **Network Tab**: Check API calls in browser DevTools
4. **Components**: Inspect component state in React DevTools

### API Integration

All API calls go through `services/api.js`:
- Centralized configuration
- Error handling
- Request/response interceptors (if needed)

### State Management

Currently using React hooks:
- `useState` for local state
- `useEffect` for side effects
- `useMemo` for computed values
- Consider Context API or Redux for complex state

## 🐛 Troubleshooting

### Common Issues

**1. Cannot connect to backend**
```
Error: Network Error
```
- Check `VITE_API_URL` in `.env`
- Ensure backend is running
- Check CORS configuration in backend

**2. Build fails**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

**3. Styles not applying**
- Check Tailwind config paths
- Restart dev server
- Clear browser cache

**4. Dark mode not working**
- Check `tailwind.config.js` has `darkMode: 'class'`
- Verify `useDarkMode` hook is used
- Check browser localStorage

**5. API calls failing in production**
- Verify `VITE_API_URL` is set in deployment platform
- Check backend CORS allows your frontend domain
- Verify backend is accessible

## 📱 Responsive Design

The app is fully responsive:
- **Mobile**: Single column layout
- **Tablet**: 2 columns
- **Desktop**: 3 columns
- Breakpoints: `sm:`, `md:`, `lg:`, `xl:`

## ♿ Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Focus indicators
- Alt text for images

## 🚀 Performance

### Optimization

- Code splitting (Vite handles automatically)
- Lazy loading for images
- Memoized components where beneficial
- Debounced search input

### Best Practices

- Keep components small and focused
- Use React.memo for expensive components
- Avoid unnecessary re-renders
- Optimize images before adding

## 📝 Adding New Features

1. **Create Component**
   ```bash
   # Create new component file
   touch src/components/NewComponent.jsx
   ```

2. **Import and Use**
   ```jsx
   import NewComponent from './components/NewComponent';
   ```

3. **Add Styles**
   - Use Tailwind classes
   - Add custom styles if needed

4. **Test**
   - Test in development
   - Test responsive design
   - Test dark mode

## 🤝 Contributing

When adding features:
1. Follow existing component structure
2. Use Tailwind for styling
3. Add dark mode support
4. Make it responsive
5. Handle loading and error states
6. Update this README if needed

---

**Happy Coding! 🎨**
