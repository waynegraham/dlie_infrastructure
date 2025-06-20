export const dynamic = 'force-dynamic'   // ← Opt out of static prerender

import Link from 'next/link'
import ExhibitCard from '@/components/ExhibitCard'

export const metadata = {
  title: 'Exhibits • Digital Library of Integral Ecology',
}

interface ExhibitSummary {
  slug: string
  title: string
  excerpt: string
  thumbnailUrl?: string
}

export default async function ExhibitsPage() {
  const base = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL
  if (!base) {
    throw new Error(
      'API URL is not configured. Please set NEXT_PUBLIC_API_URL or API_URL.'
    )
  }
  const res = await fetch(`${base}/exhibits`)
  if (!res.ok) {
    throw new Error(`Failed to fetch exhibits: ${res.status} ${res.statusText}`)
  }
  const exhibits: ExhibitSummary[] = await res.json()

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Curated Exhibits</h1>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {exhibits.map((exhibit) => (
          <Link key={exhibit.slug} href={`/exhibits/${exhibit.slug}`}>

            <ExhibitCard
              slug={exhibit.slug}
              title={exhibit.title}
              excerpt={exhibit.excerpt}
              thumbnailUrl={exhibit.thumbnailUrl}
            />

          </Link>
        ))}
      </div>
    </div>
  );
}