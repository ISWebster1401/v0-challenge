import React from 'react';
import NewsCard from './NewsCard';
import Pagination from './Pagination';

export default function NewsList({ articles, searchTerm, currentPage, totalPages, onPageChange, isFiltered }) {
  if (!articles || articles.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400 text-lg">
          {searchTerm ? 'No articles match your search. Try a different term!' : 'No articles found. Try refreshing!'}
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {articles.map((article) => (
          <NewsCard key={article.id} article={article} searchTerm={searchTerm} />
        ))}
      </div>
      {/* Only show pagination if not filtered (search/topic filters work on client side) */}
      {!isFiltered && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={onPageChange}
        />
      )}
    </>
  );
}

