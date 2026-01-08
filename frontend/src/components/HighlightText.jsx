import React from 'react';

export default function HighlightText({ text, searchTerm }) {
  if (!searchTerm || !text) {
    return <>{text}</>;
  }

  // Case-insensitive search
  const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, index) => {
        if (part.toLowerCase() === searchTerm.toLowerCase()) {
          return (
            <mark key={index} className="bg-yellow-300 dark:bg-yellow-600 dark:text-yellow-900 px-0.5 rounded">
              {part}
            </mark>
          );
        }
        return <React.Fragment key={index}>{part}</React.Fragment>;
      })}
    </>
  );
}
