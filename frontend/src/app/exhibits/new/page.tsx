'use client'
export const dynamic = 'force-dynamic'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import MarkdownEditor from '@/components/MarkdownEditor'
import ResourcePicker from '@/components/ResourcePicker'

export default function NewExhibitPage() {
  const router = useRouter()
  const [title, setTitle] = useState('')
  const [slug, setSlug] = useState('')
  const [markdown, setMarkdown] = useState('')
  const [resources, setResources] = useState<string[]>([])

  const canSave = title.trim() && slug.trim()

  const handleSave = async () => {
    if (!canSave) return
    const body = { title, slug, narrative: markdown, resources }
    const res = await fetch(`/api/exhibits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (res.ok) router.push(`/exhibits/${slug}`)
    else alert('Failed to save exhibit')
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Create New Exhibit</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <label className="block">
            <span className="font-medium">Title</span>
            <input
              type="text"
              value={title}
              onChange={e => setTitle(e.target.value)}
              className="mt-1 block w-full border rounded p-2"
              placeholder="Exhibit Title"
            />
          </label>
          <label className="block">
            <span className="font-medium">Slug</span>
            <input
              type="text"
              value={slug}
              onChange={e => setSlug(e.target.value)}
              className="mt-1 block w-full border rounded p-2"
              placeholder="exhibit-slug"
            />
          </label>
        </div>

        <div>
          <label className="block mb-2 font-medium">Narrative</label>
          <MarkdownEditor
            initialValue={markdown}
            onChange={val => setMarkdown(val)}
          />
        </div>
      </div>

      <div>
        <label className="block mb-2 font-medium">Resources</label>
        <ResourcePicker
          selected={resources}
          onChange={sel => setResources(sel)}
        />
      </div>

      <button
        disabled={!canSave}
        onClick={handleSave}
        className={`px-4 py-2 rounded text-white ${
          canSave ? 'bg-teal-600 hover:bg-teal-700' : 'bg-gray-400 cursor-not-allowed'
        }`}
      >
        Save Exhibit
      </button>
    </div>
  )
}