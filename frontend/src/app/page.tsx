// src/app/page.tsx

export const dynamic = 'force-dynamic'

import Link from 'next/link'
import SearchFormWrapper from '@/components/SearchFormWrapper'
import ExhibitCard from '@/components/ExhibitCard'
import ResourceCard from '@/components/ResourceCard'

export const metadata = {
  title: 'Digital Ecology Library',
  description: 'Discover and explore Integral Ecology resources',
}

interface ExhibitSummary {
  slug: string
  title: string
  excerpt: string
  thumbnailUrl?: string
}

interface ResourceSummary {
  id: string
  title: string
  authors: string[]
  date: string
}

export default async function HomePage() {
  const base = process.env.API_URL ?? 'http://localhost:8000'

  // Featured exhibits
  const exRes = await fetch(`${base}/exhibits?limit=4`)
  const exData = await exRes.json()
  const featured: ExhibitSummary[] = Array.isArray(exData)
    ? exData
    : (exData.items as ExhibitSummary[]) ??
      (exData.results as ExhibitSummary[]) ??
      []

  // Recently added resources (limit to last 6)
  const rRes = await fetch(`${base}/resources?limit=6`)
  const rData = await rRes.json()
  const recent: ResourceSummary[] = Array.isArray(rData)
    ? rData
    : (rData.items as ResourceSummary[]) ??
      (rData.results as ResourceSummary[]) ??
      []

  return (
    <div className="space-y-16">
      {/* Hero / Mission Section */}
      <section className="text-center py-20 bg-teal-50">
        <h1 className="text-5xl font-bold">Digital Ecology Library</h1>
        <p className="mt-4 text-xl text-gray-700">
          Discover and Explore Resources on Integral Ecology
        </p>
        <SearchFormWrapper />
      </section>
      {/* Featured Exhibits */}
      <section className="container mx-auto px-4 space-y-4">
        <h2 className="text-3xl font-semibold">Featured Exhibits</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {featured.length > 0 ? (
            featured.map((ex) => (
              <Link key={ex.slug} href={`/exhibits/${ex.slug}`}>

                <ExhibitCard
                  slug={ex.slug}
                  title={ex.title}
                  excerpt={ex.excerpt}
                  thumbnailUrl={ex.thumbnailUrl}
                />

              </Link>
            ))
          ) : (
            <p className="col-span-full text-center text-gray-500">
              No featured exhibits available.
            </p>
          )}
        </div>
      </section>
      {/* Recently Added Resources */}
      <section className="container mx-auto px-4 space-y-4">
        <h2 className="text-3xl font-semibold">Recently Added Resources</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {recent.length > 0 ? (
            recent.map((res) => (
              <ResourceCard
                key={res.id}
                id={res.id}
                title={res.title}
                authors={res.authors}
                date={res.date}
              />
            ))
          ) : (
            <p className="col-span-full text-center text-gray-500">
              No recent resources found.
            </p>
          )}
        </div>
      </section>
    </div>
  );
}