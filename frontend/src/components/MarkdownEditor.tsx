// src/components/MarkdownEditor.tsx
'use client'

import React from 'react'

export interface MarkdownEditorProps {
  initialValue: string
  onChange: (value: string) => void
}

export default function MarkdownEditor({
  initialValue,
  onChange,
}: MarkdownEditorProps) {
  return (
    <textarea
      value={initialValue}
      onChange={e => onChange(e.target.value)}
      className="w-full h-64 border rounded p-2 font-mono"
      placeholder="Write your narrative here (Markdown supported)…"
    />
  )
}