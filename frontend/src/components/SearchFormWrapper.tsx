// src/components/SearchFormWrapper.tsx
'use client'

import React from 'react'
import SearchBar from '@/components/SearchBar'

export default function SearchFormWrapper() {
  return (
    <div className="mt-6 max-w-xl mx-auto">
      <SearchBar
        initialQuery=""
        onSearch={(q) =>
          window.location.href = `/search?query=${encodeURIComponent(q)}`
        }
      />
    </div>
  )
}