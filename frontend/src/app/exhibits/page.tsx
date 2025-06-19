// src/app/exhibits/page.tsx

export const dynamic = 'force-dynamic'   // ← Opt out of static prerender

import Link from 'next/link'
import ExhibitCard from '@/components/ExhibitCard'

export const metadata = {
  title: 'Exhibits • Digital Ecology Library',
}

interface ExhibitSummary {
  slug: string
  title: string
  excerpt: string
  thumbnailUrl?: string
}

export default async function ExhibitsPage() {
  const base = process.env.API_URL ?? 'http://localhost:8000'
  const res = await fetch(`${base}/exhibits`)
  const exhibits: ExhibitSummary[] = await res.json()

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Curated Exhibits</h1>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {exhibits.map((exhibit) => (
          <Link key={exhibit.slug} href={`/exhibits/${exhibit.slug}`}>
            <a>
              <ExhibitCard
                slug={exhibit.slug}
                title={exhibit.title}
                excerpt={exhibit.excerpt}
                thumbnailUrl={exhibit.thumbnailUrl}
              />
            </a>
          </Link>
        ))}
      </div>
    </div>
  )
}