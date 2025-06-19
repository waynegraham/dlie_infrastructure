'use client'
export const dynamic = 'force-dynamic'

import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-4">404 — Page Not Found</h1>
      <p className="mb-6">Sorry, we couldn’t find what you were looking for.</p>
      <Link
        href="/"
        className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700">
        
          Go Home
        
      </Link>
    </div>
  );
}