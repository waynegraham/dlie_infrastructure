// src/components/ClientLayout.tsx
'use client'

import { SessionProvider } from 'next-auth/react'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider>
      <Header />
      {children}
      <Footer />
    </SessionProvider>
  )
}