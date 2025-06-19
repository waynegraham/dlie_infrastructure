import React from 'react'
import ResourceCard from '@/components/ResourceCard'

export interface ResourceSummary {
  id: string
  title: string
  authors: string[]
  date: string
}

export interface ExhibitDetailProps {
  title: string
  narrativeHtml: string
  resources: ResourceSummary[]
}

export default function ExhibitDetail({
  title,
  narrativeHtml,
  resources,
}: ExhibitDetailProps) {
  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">{title}</h1>
      <div
        className="prose"
        dangerouslySetInnerHTML={{ __html: narrativeHtml }}
      />

      <section>
        <h2 className="text-2xl font-semibold">Resources in this Exhibit</h2>
        <div className="grid gap-4 md:grid-cols-2">
          {resources.map((r) => (
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