import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import NewsList from './components/NewsList';
import LoadingSpinner from './components/LoadingSpinner';
import { newsAPI } from './services/api';
import { useDarkMode } from './hooks/useDarkMode';

function App() {
  const [isDark, toggleDark] = useDarkMode();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cacheAge, setCacheAge] = useState(null);
  const [fromDate, setFromDate] = useState(null);
  const [toDate, setToDate] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [topics, setTopics] = useState([]);

  // Filter articles based on search term and topic
  const filteredArticles = React.useMemo(() => {
    let filtered = articles;

    // Apply topic filter
    if (selectedTopic) {
      const topicLower = selectedTopic.toLowerCase();
      filtered = filtered.filter(article => {
        const title = article.title.toLowerCase();
        const summary = article.summary.toLowerCase();
        return title.includes(topicLower) || summary.includes(topicLower);
      });
    }

    // Apply search filter
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(article => 
        article.title.toLowerCase().includes(term) ||
        article.summary.toLowerCase().includes(term) ||
        article.source.toLowerCase().includes(term)
      );
    }

    return filtered;
  }, [articles, searchTerm, selectedTopic]);

  const fetchNews = async (from = null, to = null) => {
    try {
      setLoading(true);
      setError(null);
      const data = await newsAPI.getNews(10, from, to);
      setArticles(data.articles);
      setCacheAge(data.cache_age);
      setTopics(data.topics || []);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      console.error('Error fetching news:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      setLoading(true);
      const data = await newsAPI.refreshNews(10, fromDate, toDate);
      setArticles(data.articles);
      setCacheAge(0);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      console.error('Error refreshing news:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDateFilterChange = async (from, to) => {
    setFromDate(from);
    setToDate(to);
    await fetchNews(from, to);
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleTopicClick = (topic) => {
    if (selectedTopic === topic) {
      setSelectedTopic(null);
    } else {
      setSelectedTopic(topic);
    }
  };

  const handleClearTopic = () => {
    setSelectedTopic(null);
  };

  useEffect(() => {
    fetchNews();
  }, []);

  if (loading && articles.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-800 transition-colors duration-300">
      <Header 
        onRefresh={handleRefresh} 
        loading={loading}
        cacheAge={cacheAge}
        onDateFilterChange={handleDateFilterChange}
        isDark={isDark}
        toggleDark={toggleDark}
        onSearch={handleSearch}
        searchResultCount={filteredArticles.length}
        totalArticleCount={articles.length}
        topics={topics}
        selectedTopic={selectedTopic}
        onTopicClick={handleTopicClick}
        onClearTopic={handleClearTopic}
      />
      
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded mb-6">
            <p className="font-semibold">Error loading news</p>
            <p className="text-sm">{error}</p>
          </div>
        )}
        
        <NewsList articles={filteredArticles} searchTerm={searchTerm} />
      </main>
      
      <footer className="bg-white dark:bg-gray-800 border-t dark:border-gray-700 mt-12 py-6 transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 text-center text-gray-600 dark:text-gray-400 text-sm">
          <p>Powered by OpenAI GPT-4o-mini • NewsAPI • Built for V0 Challenge</p>
          <p className="mt-1">Sebastian Webster • 2026</p>
        </div>
      </footer>
    </div>
  );
}

export default App;

