'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import SearchBar from '@/components/SearchBar'
import FacetPanel, { FacetOption } from '@/components/FacetPanel'
import ResourceCard from '@/components/ResourceCard'
import Pagination from '@/components/Pagination'

interface ResourceSummary {
  id: string
  title: string
  authors: string[]
  date: string
}

interface SearchResponse {
  items: ResourceSummary[]
  total: number
  page_size: number
  facets?: Record<string, FacetOption[]>
}

export default function SearchClient() {
  const searchParams = useSearchParams()
  const router = useRouter()

  const query = searchParams.get('query')?.trim() || ''
  const page = parseInt(searchParams.get('page') || '1', 10)
  const pageSize = 10

  const [items, setItems] = useState<ResourceSummary[]>([])
  const [total, setTotal] = useState(0)
  const [facets, setFacets] = useState<Record<string, FacetOption[]>>({})
  const [selectedFacets, setSelectedFacets] = useState<Record<string, string[]>>({})
  const [loading, setLoading] = useState(false)

  // Use localhost:8000 in browser (host machine), container DNS internally for server
  const isBrowser = typeof window !== 'undefined'
  const base = isBrowser
    ? 'http://localhost:8000'
    : process.env.NEXT_PUBLIC_API_URL ?? process.env.API_URL
  if (!base) {
    throw new Error('Search URL is not configured. Set NEXT_PUBLIC_API_URL or API_URL.')
  }

  useEffect(() => {
    // Perform search (empty query returns all items via backend)
    setLoading(true)
    ;(async () => {
      try {
        const params = new URLSearchParams()
        params.set('query', query)
        params.set('page', String(page))
        params.set('page_size', String(pageSize))
        Object.entries(selectedFacets).forEach(([cat, vals]) => {
          vals.forEach((v) => params.append(cat, v))
        })

        const res = await fetch(`${base}/search?${params.toString()}`)
        if (!res.ok) {
          throw new Error(`Search error: ${res.status} ${res.statusText}`)
        }
        const data: SearchResponse = await res.json()
        setItems(data.items)
        setTotal(data.total)
        setFacets(data.facets ?? {})
      } catch {
        setItems([])
        setTotal(0)
        setFacets({})
      } finally {
        setLoading(false)
      }
    })()
  }, [query, page, selectedFacets])

  const onSearch = (q: string) => {
    router.push(`/search?query=${encodeURIComponent(q)}&page=1`)
  }

  const onPageChange = (p: number) => {
    router.push(`/search?query=${encodeURIComponent(query)}&page=${p}`)
  }

  const onFacetChange = (category: string, values: string[]) => {
  setSelectedFacets((prev) => ({ ...prev, [category]: values }))
  }

  const [showFacets, setShowFacets] = useState(false)

  return (
    <>
      {/* Mobile: search + toggle */}
      <div className="flex justify-between items-center mb-4 lg:hidden">
        <SearchBar initialQuery={query} onSearch={onSearch} />
        <button
          onClick={() => setShowFacets(prev => !prev)}
          aria-label="Toggle filters"
          className="p-2 focus:outline-none focus:ring"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 text-gray-700"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16M4 18h16"
            />
          </svg>
        </button>
      </div>

      {/* Mobile: facets */}
      {showFacets && (
        <div className="mb-4 lg:hidden">
          <FacetPanel facets={facets} selected={selectedFacets} onFacetChange={onFacetChange} />
        </div>
      )}

      {/* Desktop: layout */}
      <div className="hidden lg:flex lg:gap-6">
        <aside className="w-1/3">
          <FacetPanel facets={facets} selected={selectedFacets} onFacetChange={onFacetChange} />
        </aside>
        <div className="w-2/3 space-y-6">
          <SearchBar initialQuery={query} onSearch={onSearch} />

          {loading ? (
            <p>Loading…</p>
          ) : items.length > 0 ? (
            items.map(r => (
              <ResourceCard key={r.id} id={r.id} title={r.title} authors={r.authors} date={r.date} />
            ))
          ) : (
            <p className="text-gray-600">No results found.</p>
          )}
        </div>
      </div>

      {/* Mobile: results */}
      {!showFacets && (
        <div className="space-y-6 lg:hidden">
          {loading ? (
            <p>Loading…</p>
          ) : items.length > 0 ? (
            items.map(r => (
              <ResourceCard key={r.id} id={r.id} title={r.title} authors={r.authors} date={r.date} />
            ))
          ) : (
            <p className="text-gray-600">No results found.</p>
          )}
        </div>
      )}

      {/* Pagination */}
      <div className="mt-6">
        <Pagination
          currentPage={page}
          totalPages={Math.ceil(total / pageSize)}
          pageSize={pageSize}
          totalItems={total}
          onPageChange={onPageChange}
        />
      </div>
    </>
  )
}