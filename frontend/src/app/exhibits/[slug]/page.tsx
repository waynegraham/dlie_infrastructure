'use client'

import { useParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import ResourceCard from '@/components/ResourceCard'

interface Exhibit {
  title: string
  narrative: string
  resources: Array<{
    id: string
    title: string
    authors: string[]
    date: string
  }>
}

export default function ExhibitPage() {
  const { slug } = useParams() as { slug: string }
  const [exhibit, setExhibit] = useState<Exhibit | null>(null)

  useEffect(() => {
    if (!slug) return
    fetch(`${process.env.API_URL}/exhibits/${slug}`)
      .then((res) => res.json())
      .then((data: Exhibit) => setExhibit(data))
  }, [slug])

  if (!exhibit) return <p>Loading…</p>

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">{exhibit.title}</h1>
      <div
        className="prose"
        dangerouslySetInnerHTML={{ __html: exhibit.narrative }}
      />
      <section>
        <h2 className="text-2xl font-semibold">Resources in this Exhibit</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {exhibit.resources.map((r) => (
            <ResourceCard
              key={r.id}
              id={r.id}
              title={r.title}
              authors={r.authors}
              date={r.date}
            />
          ))}
        </div>
      </section>
    </div>
  )
}