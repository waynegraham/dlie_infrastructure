export const dynamic = 'force-dynamic'

import Link from 'next/link'
import SearchFormWrapper from '@/components/SearchFormWrapper'
import ExhibitCard from '@/components/ExhibitCard'
import ResourceCard from '@/components/ResourceCard'
import Hero from '@/components/Hero'

export const metadata = {
  title: 'Digital Library of Integral Ecology',
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
  const base = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL
  if (!base) {
    throw new Error(
      'API URL is not configured. Please set NEXT_PUBLIC_API_URL or API_URL.'
    )
  }

  // Featured exhibits
  const exRes = await fetch(`${base}/exhibits?limit=4`)
  if (!exRes.ok) {
    throw new Error(`Failed to fetch exhibits: ${exRes.status} ${exRes.statusText}`)
  }
  const exData = await exRes.json()
  const featured: ExhibitSummary[] = Array.isArray(exData)
    ? exData
    : (exData.items as ExhibitSummary[]) ??
      (exData.results as ExhibitSummary[]) ??
      []

  // Recently added resources (limit to last 6)
  const rRes = await fetch(`${base}/resources?limit=6`)
  if (!rRes.ok) {
    throw new Error(`Failed to fetch resources: ${rRes.status} ${rRes.statusText}`)
  }
  const rData = await rRes.json()
  const recent: ResourceSummary[] = Array.isArray(rData)
    ? rData
    : (rData.items as ResourceSummary[]) ??
      (rData.results as ResourceSummary[]) ??
      []

  return (
    
    <div className="space-y-16">

      {/* Hero / Mission Section */}
      {/* Hero Component */}
      <Hero />

      <section className="relative w-screen left-1/2 -translate-x-1/2 text-center py-16 bg-teal-50 overflow-hidden">
        {/* subtle diagonal pattern overlay */}
        <div className="absolute inset-0 bg-[repeating-linear-gradient(45deg,rgba(255,255,255,0.15),rgba(255,255,255,0.15)_1px,transparent_1px,transparent_8px)] pointer-events-none" />
        <div className="relative container mx-auto px-4">
          <h1 className="text-5xl font-bold">Digital Library of Integral Ecology</h1>
          <p className="mt-4 text-xl text-gray-700">
            Discover and Explore Resources on Integral Ecology
          </p>
          <SearchFormWrapper />
        </div>
      </section>

      

      {/* Featured Exhibits */}
      <section className="space-y-4">
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
      <section className="space-y-4">
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