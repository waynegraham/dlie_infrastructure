'use client'

import { useSession } from 'next-auth/react'
import { useRouter }  from 'next/navigation'
import { useEffect, useState } from 'react'
import MarkdownEditor       from '@/components/MarkdownEditor'
import ResourcePicker       from '@/components/ResourcePicker'

export default function NewExhibitClient() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [selectedResources, setSelectedResources] = useState<string[]>([])

  // redirect if not signed in
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/api/auth/signin?callbackUrl=/exhibits/new')
    }
  }, [status, router])

  if (status === 'loading') return <p>Loading…</p>
  if (!session) return null

  return (
    <div className="py-8 space-y-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold">Create a New Exhibit</h1>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Title</h2>
        <input
          type="text"
          placeholder="Exhibit Title"
          className="w-full border rounded p-2"
        />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Narrative</h2>
        <MarkdownEditor placeholder="Write your exhibit narrative here…" />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-semibold">Add Resources</h2>
        <ResourcePicker
          selected={selectedResources}
          onChange={setSelectedResources}
        />
      </section>

      <button
        type="submit"
        className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700"
      >
        Save Exhibit
      </button>
    </div>
  )
}