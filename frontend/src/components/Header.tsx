// src/components/Header.tsx
'use client'

import { SessionProvider, useSession, signIn, signOut } from 'next-auth/react'
import Link from 'next/link'
import Image from 'next/image'

// Wrap the actual header in SessionProvider
export default function Header() {
  return (
    <SessionProvider>
      <HeaderContent />
    </SessionProvider>
  )
}

// HeaderContent is a true function component, so hooks are valid here
function HeaderContent() {
  const { data: session } = useSession()

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
        {/* Logo + Home */}
        <Link href="/">
          <a className="flex items-center">
            <Image src="/logo.png" alt="Digital Ecology Logo" width={40} height={40} />
            <span className="ml-2 text-xl font-semibold">Digital Library of Integral Ecology</span>
          </a>
        </Link>

        {/* Nav Links */}
        <nav className="space-x-4">
          <Link href="/exhibits"><a className="hover:text-teal-600">Exhibits</a></Link>
          <Link href="/about"><a className="hover:text-teal-600">About</a></Link>
          <Link href="/search"><a className="hover:text-teal-600">Search</a></Link>
        </nav>

        {/* Auth Button */}
        <div>
          {session ? (
            <button
              onClick={() => signOut()}
              className="px-3 py-1 border rounded hover:bg-gray-100"
            >
              Sign out
            </button>
          ) : (
            <button
              onClick={() => signIn('google')}
              className="px-3 py-1 border rounded hover:bg-gray-100"
            >
              Sign in
            </button>
          )}
        </div>
      </div>
    </header>
  )
}