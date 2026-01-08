import React, { useState, useEffect, useRef } from 'react';
import { newsAPI } from '../services/api';

export default function FullSummaryModal({ isOpen, onClose, summary, wordCount, articleUrl, articleTitle, loading, error }) {
  const [selectedText, setSelectedText] = useState('');
  const [showExplainButton, setShowExplainButton] = useState(false);
  const [explanation, setExplanation] = useState(null);
  const [loadingExplanation, setLoadingExplanation] = useState(false);
  const [explanationError, setExplanationError] = useState(null);
  const [buttonPosition, setButtonPosition] = useState({ top: 0, left: 0 });
  const summaryRef = useRef(null);

  // Reset state when modal closes
  useEffect(() => {
    if (!isOpen) {
      setSelectedText('');
      setShowExplainButton(false);
      setExplanation(null);
      setExplanationError(null);
    }
  }, [isOpen]);

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();

      if (text.length >= 10) {
        setSelectedText(text);
        
        // Get selection position
        if (selection.rangeCount > 0) {
          const range = selection.getRangeAt(0);
          const rect = range.getBoundingClientRect();
          const modalRect = summaryRef.current?.getBoundingClientRect();
          
          if (modalRect) {
            setButtonPosition({
              top: rect.bottom - modalRect.top + 10,
              left: rect.left - modalRect.left
            });
            setShowExplainButton(true);
          }
        }
      } else {
        setShowExplainButton(false);
        setSelectedText('');
      }
    };

    const handleClickOutside = (e) => {
      if (summaryRef.current && !summaryRef.current.contains(e.target)) {
        setShowExplainButton(false);
        setSelectedText('');
      }
    };

    if (isOpen && summary) {
      document.addEventListener('selectionchange', handleSelection);
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('selectionchange', handleSelection);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, summary]);

  const handleExplainBetter = async () => {
    if (!selectedText || selectedText.length < 10) return;

    try {
      setLoadingExplanation(true);
      setExplanationError(null);
      const data = await newsAPI.explainText(selectedText, summary);
      setExplanation(data.explanation);
      setShowExplainButton(false);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to generate explanation';
      setExplanationError(errorMessage);
      console.error('Error generating explanation:', err);
    } finally {
      setLoadingExplanation(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        {/* Background overlay */}
        <div 
          className="fixed inset-0 bg-gray-500 bg-opacity-75 dark:bg-gray-900 dark:bg-opacity-75 transition-opacity"
          onClick={onClose}
        ></div>

        {/* Modal panel */}
        <div className="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
          <div className="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100" id="modal-title">
                {articleTitle || 'Full Article Summary'}
              </h3>
              <button
                onClick={onClose}
                className="text-gray-400 dark:text-gray-500 hover:text-gray-500 dark:hover:text-gray-400 focus:outline-none"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {loading && (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600 dark:border-blue-400"></div>
                <p className="mt-4 text-gray-600 dark:text-gray-400 font-semibold">Generating comprehensive summary...</p>
                <p className="mt-2 text-gray-500 dark:text-gray-500 text-sm">This may take a few seconds</p>
              </div>
            )}

            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded mb-4">
                <p className="font-semibold">Error generating summary</p>
                <p className="text-sm mt-1">{error}</p>
              </div>
            )}

            {summary && !loading && (
              <div className="relative" ref={summaryRef}>
                <div className="flex items-center justify-between mb-4 text-sm text-gray-600 dark:text-gray-400">
                  <span className="font-semibold">Comprehensive Summary</span>
                  <span>{wordCount} words</span>
                </div>
                
                {/* Explain button - appears when text is selected */}
                {showExplainButton && (
                  <button
                    onClick={handleExplainBetter}
                    disabled={loadingExplanation}
                    className="absolute z-10 px-3 py-1.5 bg-blue-600 dark:bg-blue-500 text-white text-sm font-semibold rounded-md shadow-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    style={{
                      top: `${buttonPosition.top}px`,
                      left: `${buttonPosition.left}px`,
                    }}
                  >
                    {loadingExplanation ? (
                      <>
                        <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Explaining...
                      </>
                    ) : (
                      <>
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Explain Better
                      </>
                    )}
                  </button>
                )}

                {/* Explanation result */}
                {explanation && (
                  <div className="mb-4 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-blue-900 dark:text-blue-200">Detailed Explanation</h4>
                      <button
                        onClick={() => setExplanation(null)}
                        className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    <p className="text-blue-800 dark:text-blue-300 text-sm leading-relaxed whitespace-pre-wrap">
                      {explanation}
                    </p>
                  </div>
                )}

                {explanationError && (
                  <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded">
                    <p className="font-semibold text-sm">Error generating explanation</p>
                    <p className="text-xs mt-1">{explanationError}</p>
                  </div>
                )}

                <div className="prose max-w-none">
                  <p 
                    className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap select-text"
                    style={{ userSelect: 'text' }}
                  >
                    {summary}
                  </p>
                </div>
              </div>
            )}

            {articleUrl && (
              <div className="mt-6 pt-4 border-t dark:border-gray-700">
                <a
                  href={articleUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-semibold"
                >
                  Read original article
                  <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </a>
              </div>
            )}
          </div>
          
          <div className="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="button"
              onClick={onClose}
              className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 dark:bg-blue-700 text-base font-medium text-white hover:bg-blue-700 dark:hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
