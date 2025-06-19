// src/components/Footer.tsx
'use client'

import React from 'react'

export default function Footer() {
  return (
    <footer className="bg-gray-100 text-gray-600 py-6 mt-12">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-sm">
          &copy; {new Date().getFullYear()} Digital Ecology Library. All rights reserved.
        </p>
        <nav className="mt-2 space-x-4">
          <a href="/about" className="hover:text-teal-600">About</a>
          <a href="https://github.com/your-repo" className="hover:text-teal-600">GitHub</a>
          <a href="/privacy" className="hover:text-teal-600">Privacy</a>
        </nav>
      </div>
    </footer>
  )
}