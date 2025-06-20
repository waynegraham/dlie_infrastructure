export const dynamic = 'force-dynamic'

import Link from 'next/link'
import ResourceCard from '@/components/ResourceCard'

export const metadata = {
  title: 'Resources • Digital Library of Integral Ecology',
}

interface ResourceSummary {
  id: string
  title: string
  authors: string[]
  date: string
}

export default async function ResourcesPage() {
  const base = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL
  if (!base) {
    throw new Error(
      'API URL is not configured. Please set NEXT_PUBLIC_API_URL or API_URL.'
    )
  }

  const res = await fetch(`${base}/resources?limit=1000`)
  if (!res.ok) {
    throw new Error(`Failed to fetch resources: ${res.status} ${res.statusText}`)
  }
  const data = await res.json()
  const resources: ResourceSummary[] =
    Array.isArray(data) ? data : (data.items as ResourceSummary[]) ?? []

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">All Resources</h1>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {resources.map((r) => (
          <Link key={r.id} href={`/resources/${r.id}`}>
            <ResourceCard
              id={r.id}
              title={r.title}
              authors={r.authors}
              date={r.date}
            />
          </Link>
        ))}
      </div>
    </div>
  )
}