import React from 'react';

export default function TrendingTopics({ topics, selectedTopic, onTopicClick, onClear }) {
  if (!topics || topics.length === 0) {
    return null;
  }

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <span className="text-sm font-semibold text-blue-100 dark:text-blue-200">Trending:</span>
      {topics.map((topic) => (
        <button
          key={topic}
          onClick={() => onTopicClick(topic)}
          className={`px-3 py-1 rounded-full text-sm font-medium transition-all duration-200 ${
            selectedTopic === topic
              ? 'bg-white text-blue-600 dark:bg-gray-700 dark:text-blue-400 shadow-md scale-105'
              : 'bg-white/20 text-white hover:bg-white/30 hover:scale-105'
          }`}
        >
          {topic}
        </button>
      ))}
      {selectedTopic && (
        <button
          onClick={onClear}
          className="px-3 py-1 rounded-full text-sm font-medium bg-white/20 text-white hover:bg-white/30 transition-all duration-200 flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
          Clear
        </button>
      )}
    </div>
  );
}
