'use client'

import React from 'react'

export interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  /** Number of items shown per page */
  pageSize: number;
  /** Total number of items */
  totalItems: number;
}

export default function Pagination({ currentPage, totalPages, onPageChange, pageSize, totalItems }: PaginationProps) {
  if (totalPages <= 1) return null;

  // Summary of results
  const end = Math.min(currentPage * pageSize, totalItems);
  const summary = `Showing ${end} of ${totalItems} results`;

  // Build truncated page list: first 3, ellipsis if needed, last 3
  const pages: (number | string)[] = [];
  for (let i = 1; i <= Math.min(3, totalPages); i++) pages.push(i);
  if (totalPages > 6) pages.push('...');
  for (let i = Math.max(4, totalPages - 2); i <= totalPages; i++) pages.push(i);

  return (
    <nav aria-label="Pagination" className="flex items-center justify-between">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-3 py-1 border rounded disabled:opacity-50"
      >
        &laquo;
      </button>

      <div className="text-sm text-gray-600">{summary}</div>

      <div className="flex items-center space-x-1">
        {pages.map((p, idx) =>
          p === '...' ? (
            <span key={`ellipsis-${idx}`} className="px-2 text-gray-500">
              …
            </span>
          ) : (
            <button
              key={p}
              onClick={() => onPageChange(p as number)}
              className={`px-3 py-1 border rounded ${
                p === currentPage ? 'bg-teal-600 text-white' : 'hover:bg-gray-100'
              }`}
            >
              {p}
            </button>
          )
        )}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-3 py-1 border rounded disabled:opacity-50"
      >
        &raquo;
      </button>
    </nav>
  );
}