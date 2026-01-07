import React from 'react';

export default function Header({ onRefresh, loading, cacheAge }) {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">🚀 Tech News Summarizer</h1>
            <p className="text-blue-100 text-sm mt-1">
              AI-powered summaries of the hottest tech news
            </p>
          </div>
          <button
            onClick={onRefresh}
            disabled={loading}
            className="bg-white text-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? '⏳ Loading...' : '🔄 Refresh'}
          </button>
        </div>
        {cacheAge !== null && (
          <p className="text-blue-100 text-xs mt-2">
            Last updated: {Math.floor(cacheAge / 60)} minutes ago
          </p>
        )}
      </div>
    </header>
  );
}

