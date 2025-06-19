import React, { Suspense } from 'react'
import SearchClient from './SearchClient'

export const dynamic = 'force-dynamic'

export default function SearchPage() {
  return (
    <Suspense fallback={<p className="p-4 text-center">Loading search…</p>}>
      <SearchClient />
    </Suspense>
  )
}