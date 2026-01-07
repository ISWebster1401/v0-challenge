import { useState, useEffect } from 'react';
import Header from './components/Header';
import NewsList from './components/NewsList';
import LoadingSpinner from './components/LoadingSpinner';
import { newsAPI } from './services/api';

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cacheAge, setCacheAge] = useState(null);

  const fetchNews = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await newsAPI.getNews(10);
      setArticles(data.articles);
      setCacheAge(data.cache_age);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching news:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      setLoading(true);
      const data = await newsAPI.refreshNews();
      setArticles(data.articles);
      setCacheAge(0);
    } catch (err) {
      setError(err.message);
      console.error('Error refreshing news:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, []);

  if (loading && articles.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onRefresh={handleRefresh} 
        loading={loading}
        cacheAge={cacheAge}
      />
      
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            <p className="font-semibold">Error loading news</p>
            <p className="text-sm">{error}</p>
          </div>
        )}
        
        <NewsList articles={articles} />
      </main>
      
      <footer className="bg-white border-t mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600 text-sm">
          <p>Powered by OpenAI GPT-4o-mini • NewsAPI • Built for V0 Challenge</p>
          <p className="mt-1">Sebastian Webster • 2026</p>
        </div>
      </footer>
    </div>
  );
}

export default App;

