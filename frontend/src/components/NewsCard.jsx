import React, { useState } from 'react';
import { newsAPI } from '../services/api';
import FullSummaryModal from './FullSummaryModal';

export default function NewsCard({ article }) {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const [fullSummary, setFullSummary] = useState(null);
  const [loadingFullSummary, setLoadingFullSummary] = useState(false);
  const [fullSummaryError, setFullSummaryError] = useState(null);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleFullSummary = async () => {
    setShowFullSummary(true);
    setFullSummaryError(null);
    
    // Check if we already have a cached summary
    if (fullSummary) {
      return;
    }

    try {
      setLoadingFullSummary(true);
      const data = await newsAPI.getFullSummary(article.url);
      setFullSummary(data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to generate full summary';
      setFullSummaryError(errorMessage);
      console.error('Error generating full summary:', err);
    } finally {
      setLoadingFullSummary(false);
    }
  };

  return (
    <>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 flex flex-col">
        {article.imageUrl && (
          <div className="w-full h-48 bg-gray-200 flex-shrink-0">
            <img 
              src={article.imageUrl} 
              alt={article.title}
              className="w-full h-full object-cover"
              onError={(e) => {
                e.target.parentElement.style.display = 'none';
              }}
            />
          </div>
        )}
        <div className="p-6">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-blue-600 uppercase">
              {article.source}
            </span>
            <span className="text-xs text-gray-500">
              {formatDate(article.publishedAt)}
            </span>
          </div>
          
          <h3 className="text-xl font-bold text-gray-900 mb-3 line-clamp-2">
            {article.title}
          </h3>
          
          <p className="text-gray-600 mb-4 line-clamp-3">
            {article.summary}
          </p>
          
          <div className="flex flex-col gap-2">
            <button
              onClick={handleFullSummary}
              disabled={loadingFullSummary}
              className="inline-flex items-center justify-center px-4 py-2 bg-purple-600 text-white rounded-md font-semibold hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            >
              {loadingFullSummary ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Generating...
                </>
              ) : (
                <>
                  📚 Full Summary
                </>
              )}
            </button>
            
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center text-blue-600 hover:text-blue-800 font-semibold text-sm"
            >
              Read full article
              <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        </div>
      </div>

      <FullSummaryModal
        isOpen={showFullSummary}
        onClose={() => setShowFullSummary(false)}
        summary={fullSummary?.summary || null}
        wordCount={fullSummary?.word_count || 0}
        articleUrl={article.url}
        articleTitle={article.title}
        loading={loadingFullSummary}
        error={fullSummaryError}
      />
    </>
  );
}

