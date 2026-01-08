import React, { useState } from 'react';

export default function DateFilter({ onFilterChange, loading }) {
  const [filterType, setFilterType] = useState('all');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');

  const handleFilterTypeChange = (type) => {
    setFilterType(type);
    
    // Get current date in Chile timezone (UTC-3)
    const now = new Date();
    const chileOffset = -3 * 60; // Chile is UTC-3
    const localOffset = now.getTimezoneOffset();
    const chileTime = new Date(now.getTime() + (localOffset + chileOffset) * 60000);
    
    const today = new Date(chileTime.getFullYear(), chileTime.getMonth(), chileTime.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const lastWeek = new Date(today);
    lastWeek.setDate(lastWeek.getDate() - 7);

    const formatDate = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    };

    switch (type) {
      case 'today':
        onFilterChange(formatDate(today), formatDate(today));
        setFromDate(formatDate(today));
        setToDate(formatDate(today));
        break;
      case 'yesterday':
        onFilterChange(formatDate(yesterday), formatDate(yesterday));
        setFromDate(formatDate(yesterday));
        setToDate(formatDate(yesterday));
        break;
      case 'last7days':
        onFilterChange(formatDate(lastWeek), formatDate(today));
        setFromDate(formatDate(lastWeek));
        setToDate(formatDate(today));
        break;
      case 'custom':
        // Don't apply filter yet, wait for user to set dates
        setFromDate('');
        setToDate('');
        break;
      case 'all':
      default:
        onFilterChange(null, null);
        setFromDate('');
        setToDate('');
        break;
    }
  };

  const handleApplyCustom = () => {
    if (fromDate && toDate) {
      if (new Date(fromDate) > new Date(toDate)) {
        alert('From date must be before or equal to to date');
        return;
      }
      onFilterChange(fromDate, toDate);
    } else if (fromDate) {
      onFilterChange(fromDate, null);
    } else if (toDate) {
      onFilterChange(null, toDate);
    }
  };

  // Get max date for date inputs (today in Chile)
  const now = new Date();
  const chileOffset = -3 * 60;
  const localOffset = now.getTimezoneOffset();
  const chileTime = new Date(now.getTime() + (localOffset + chileOffset) * 60000);
  const maxDate = `${chileTime.getFullYear()}-${String(chileTime.getMonth() + 1).padStart(2, '0')}-${String(chileTime.getDate()).padStart(2, '0')}`;

  return (
    <div className="flex flex-wrap gap-2 items-center">
      <label className="text-sm font-semibold text-blue-100 dark:text-blue-200">Filter by date:</label>
      <select
        value={filterType}
        onChange={(e) => handleFilterTypeChange(e.target.value)}
        disabled={loading}
        className="px-3 py-1.5 border border-white/30 dark:border-white/20 rounded-md text-sm bg-white/20 dark:bg-white/10 text-white focus:outline-none focus:ring-2 focus:ring-white/50 disabled:opacity-50"
      >
        <option value="all" className="bg-gray-800 text-white">All News</option>
        <option value="today" className="bg-gray-800 text-white">Today</option>
        <option value="yesterday" className="bg-gray-800 text-white">Yesterday</option>
        <option value="last7days" className="bg-gray-800 text-white">Last 7 Days</option>
        <option value="custom" className="bg-gray-800 text-white">Custom Range</option>
      </select>

      {filterType === 'custom' && (
        <>
          <input
            type="date"
            value={fromDate}
            onChange={(e) => setFromDate(e.target.value)}
            max={toDate || maxDate}
            disabled={loading}
            className="px-3 py-1.5 border border-white/30 dark:border-white/20 rounded-md text-sm bg-white/20 dark:bg-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 disabled:opacity-50"
            placeholder="From date"
          />
          <span className="text-blue-100 dark:text-blue-200 font-medium">to</span>
          <input
            type="date"
            value={toDate}
            onChange={(e) => setToDate(e.target.value)}
            min={fromDate}
            max={maxDate}
            disabled={loading}
            className="px-3 py-1.5 border border-white/30 dark:border-white/20 rounded-md text-sm bg-white/20 dark:bg-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/50 disabled:opacity-50"
            placeholder="To date"
          />
          <button
            onClick={handleApplyCustom}
            disabled={loading || (!fromDate && !toDate)}
            className="px-4 py-1.5 bg-white/20 text-white rounded-md text-sm font-semibold hover:bg-white/30 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Apply
          </button>
        </>
      )}
    </div>
  );
}

