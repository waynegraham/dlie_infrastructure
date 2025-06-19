'use client'

import { useSession, signIn, signOut } from 'next-auth/react'
import Link from 'next/link'

export default function Header() {
  const { data: session, status } = useSession()

  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold">
          Digital Library of Integral Ecology
        </Link>

        <nav className="flex items-center space-x-6">
          <Link href="/search" className="hover:underline">
            Search
          </Link>
          <Link href="/exhibits" className="hover:underline">
            Exhibits
          </Link>

          {status === 'authenticated' && (
            <Link
              href="/exhibits/new"
              className="px-3 py-1 rounded-md bg-teal-600 text-white hover:bg-teal-700"
            >
              New Exhibit
            </Link>
          )}

          {status === 'loading' ? (
            <p className="italic text-gray-500">Checking auth…</p>
          ) : session ? (
            <button
              onClick={() => signOut({ callbackUrl: '/' })}
              className="hover:underline"
            >
              Sign out
            </button>
          ) : (
            <button
              onClick={() => signIn('google')}
              className="hover:underline"
            >
              Sign in
            </button>
          )}
        </nav>
      </div>
    </header>
  )
}