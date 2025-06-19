// src/app/resources/[id]/page.tsx
'use client'

import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import Metadata from '@/components/Metadata'

interface Resource {
  title: string
  authors: string[]
  date: string
  doi?: string
  provider: string
  keywords: string[]
  abstract: string
  fulltext?: string
  url?: string
}

export default function ResourcePage() {
  const { id } = useParams() as { id: string }
  const [resource, setResource] = useState<Resource | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    ;(async () => {
      try {
        const base = 'http://localhost:8000'

        const res = await fetch(`${base}/resources/${id}`)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = (await res.json()) as Resource
        setResource(data)
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : String(err))
      } finally {
        setLoading(false)
      }
    })()
  }, [id])

  if (loading)   return <p>Loading…</p>
  if (error)     return <p className="text-red-600">Error: {error}</p>
  if (!resource) return <p>No resource found.</p>

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">{resource.title}</h1>
      <Metadata
        authors={resource.authors}
        date={resource.date}
        doi={resource.doi}
        provider={resource.provider}
        keywords={resource.keywords}
        url={resource.url}
      />
      <section>
        <h2 className="text-2xl font-semibold">Abstract</h2>
        <p>{resource.abstract}</p>
      </section>
    </div>
  )
}