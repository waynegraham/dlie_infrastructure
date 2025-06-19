'use client'

import React, { useState } from 'react'

export interface SearchBarProps {
  initialQuery?: string;
  onSearch: (query: string) => void;
}

export default function SearchBar({ initialQuery = '', onSearch }: SearchBarProps) {
  const [query, setQuery] = useState(initialQuery)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSearch(query.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="flex items-center space-x-2">
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search resources..."
        className="flex-grow border rounded p-2 focus:outline-none focus:ring-2 focus:ring-teal-600"
        aria-label="Search query"
      />
      <button
        type="submit"
        className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-teal-600"
      >
        Search
      </button>
    </form>
  )
}