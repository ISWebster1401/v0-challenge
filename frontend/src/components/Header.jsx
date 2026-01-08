import React from 'react';
import DateFilter from './DateFilter';
import SearchBar from './SearchBar';
import TrendingTopics from './TrendingTopics';

export default function Header({ onRefresh, loading, cacheAge, onDateFilterChange, isDark, toggleDark, onSearch, searchResultCount, totalArticleCount, topics, selectedTopic, onTopicClick, onClearTopic }) {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-800 dark:to-purple-800 text-white shadow-lg transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-2">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Tech News Summarizer
            </h1>
            <p className="text-blue-100 dark:text-blue-200 text-sm mt-1">
              AI-powered summaries of the hottest tech news
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={toggleDark}
              className="p-2 rounded-lg bg-white/20 hover:bg-white/30 transition-colors"
              aria-label="Toggle dark mode"
            >
              {isDark ? (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              ) : (
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                </svg>
              )}
            </button>
            <button
              onClick={onRefresh}
              disabled={loading}
              className="bg-white text-blue-600 dark:bg-gray-700 dark:text-white px-4 py-2 rounded-lg font-semibold hover:bg-blue-50 dark:hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Loading...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span>Refresh</span>
                </>
              )}
            </button>
          </div>
        </div>
        {cacheAge !== null && (
          <p className="text-blue-100 dark:text-blue-200 text-xs mt-2">
            Last updated: {Math.floor(cacheAge / 60)} minutes ago
          </p>
        )}
        <SearchBar 
          onSearch={onSearch} 
          resultCount={searchResultCount || 0}
          totalCount={totalArticleCount || 0}
        />
        <div className="flex flex-wrap items-center gap-4 mt-4">
          <TrendingTopics
            topics={topics || []}
            selectedTopic={selectedTopic}
            onTopicClick={onTopicClick}
            onClear={onClearTopic}
          />
          <DateFilter onFilterChange={onDateFilterChange} loading={loading} />
        </div>
      </div>
    </header>
  );
}

