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
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Import topic extractor keywords for better filtering
  const topicKeywords = {
    'AI': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'neural network', 'deep learning', 'gpt', 'chatgpt', 'llm', 'openai', 'claude', 'gemini'],
    'Crypto': ['crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'blockchain', 'nft', 'web3', 'defi', 'btc', 'eth'],
    'Hardware': ['hardware', 'cpu', 'gpu', 'processor', 'chip', 'intel', 'amd', 'nvidia', 'qualcomm', 'apple silicon', 'm1', 'm2', 'm3'],
    'Software': ['software', 'app', 'application', 'os', 'operating system', 'windows', 'linux', 'macos', 'ios', 'android'],
    'Startup': ['startup', 'unicorn', 'ipo', 'funding', 'venture capital', 'vc', 'series a', 'series b', 'seed round'],
    'Gaming': ['gaming', 'game', 'playstation', 'xbox', 'nintendo', 'steam', 'esports', 'gamer', 'console'],
    'Security': ['security', 'cybersecurity', 'hack', 'breach', 'vulnerability', 'malware', 'ransomware', 'phishing'],
    'Cloud': ['cloud', 'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'serverless', 'kubernetes'],
    'Mobile': ['mobile', 'smartphone', 'iphone', 'android phone', 'samsung', 'apple', 'ios', 'android'],
    'Social Media': ['twitter', 'facebook', 'instagram', 'tiktok', 'linkedin', 'social media', 'meta'],
    'Electric Vehicles': ['ev', 'electric vehicle', 'tesla', 'electric car', 'battery', 'charging'],
    'Space': ['space', 'nasa', 'spacex', 'rocket', 'satellite', 'mars', 'moon', 'astronaut']
  };

  // Filter articles based on search term only (topic filtering is now done server-side)
  const filteredArticles = React.useMemo(() => {
    let filtered = articles;

    // Apply search filter (topic filtering is done server-side when topic is selected)
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(article => 
        article.title.toLowerCase().includes(term) ||
        article.summary.toLowerCase().includes(term) ||
        article.source.toLowerCase().includes(term)
      );
    }

    return filtered;
  }, [articles, searchTerm]);

  const fetchNews = async (from = null, to = null, page = 1, topic = null) => {
    try {
      setLoading(true);
      setError(null);
      const data = await newsAPI.getNews(10, from, to, page, topic);
      setArticles(data.articles);
      setCacheAge(data.cache_age);
      setTopics(data.topics || []);
      setCurrentPage(data.current_page || 1);
      setTotalPages(data.total_pages || 1);
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
      setCurrentPage(1); // Reset to first page on refresh
      const data = await newsAPI.refreshNews(10, fromDate, toDate, 1);
      setArticles(data.articles);
      setCacheAge(0);
      setTopics(data.topics || []);
      setTotalPages(data.total_pages || 1);
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
    setCurrentPage(1); // Reset to first page on date change
    // Keep topic filter if one is selected
    await fetchNews(from, to, 1, selectedTopic);
  };

  const handlePageChange = async (page) => {
    setCurrentPage(page);
    await fetchNews(fromDate, toDate, page);
    // Scroll to top when page changes
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleTopicClick = async (topic) => {
    if (selectedTopic === topic) {
      // Deselect topic - fetch without topic filter
      setSelectedTopic(null);
      setCurrentPage(1);
      await fetchNews(fromDate, toDate, 1, null);
    } else {
      // Select topic - fetch with topic filter
      setSelectedTopic(topic);
      setCurrentPage(1);
      await fetchNews(fromDate, toDate, 1, topic);
    }
  };

  const handleClearTopic = async () => {
    setSelectedTopic(null);
    setCurrentPage(1);
    await fetchNews(fromDate, toDate, 1, null);
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
        
        <NewsList 
          articles={filteredArticles} 
          searchTerm={searchTerm}
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          isFiltered={searchTerm.trim() !== '' || selectedTopic !== null}
        />
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

