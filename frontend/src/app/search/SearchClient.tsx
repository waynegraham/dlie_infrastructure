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

  const query = searchParams.get('query') || ''
  const page  = parseInt(searchParams.get('page') || '1', 10)
  const pageSize = 10

  const [items, setItems] = useState<ResourceSummary[]>([])
  const [total, setTotal] = useState(0)
  const [facets, setFacets] = useState<Record<string, FacetOption[]>>({})
  const [selectedFacets, setSelectedFacets] = useState<Record<string, string[]>>({})
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/search?query=${encodeURIComponent(query)}&page=${page}&page_size=${pageSize}`
    )
      .then(res => res.json())
      .then((data: SearchResponse) => {
        setItems(data.items)
        setTotal(data.total)
        if (data.facets) setFacets(data.facets)
      })
      .finally(() => setLoading(false))
  }, [query, page])

  const onSearch = (q: string) => {
    router.push(`/search?query=${encodeURIComponent(q)}&page=1`)
  }

  const onPageChange = (p: number) => {
    router.push(`/search?query=${encodeURIComponent(query)}&page=${p}`)
  }

  const onFacetChange = (category: string, values: string[]) => {
    setSelectedFacets(prev => ({ ...prev, [category]: values }))
    // TODO: re‐fetch including facet filters
  }

  return (
    <div className="flex flex-col lg:flex-row container mx-auto px-4 py-6 gap-6">
      <aside className="lg:w-1/4">
        <FacetPanel
          facets={facets}
          selected={selectedFacets}
          onFacetChange={onFacetChange}
        />
      </aside>

      <div className="flex-1 space-y-6">
        <SearchBar initialQuery={query} onSearch={onSearch} />

        {loading
          ? <p>Loading…</p>
          : items.length > 0
            ? items.map(r => (
                <ResourceCard
                  key={r.id}
                  id={r.id}
                  title={r.title}
                  authors={r.authors}
                  date={r.date}
                />
              ))
            : <p className="text-gray-600">No results found.</p>
        }

        <Pagination
          currentPage={page}
          totalPages={Math.ceil(total / pageSize)}
          onPageChange={onPageChange}
        />
      </div>
    </div>
  )
}