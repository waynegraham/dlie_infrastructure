// src/components/MarkdownEditor.tsx
'use client'

import { useState } from 'react'

export interface MarkdownEditorProps {
  /** Initial markdown text */
  initialValue?: string
  /** Optional placeholder for the textarea */
  placeholder?: string
  /** Callback whenever the content changes */
  onChange?: (value: string) => void
}

export default function MarkdownEditor({
  initialValue = '',
  placeholder = '',
  onChange,
}: MarkdownEditorProps) {
  const [value, setValue] = useState(initialValue)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value)
    if (onChange) onChange(e.target.value)
  }

  return (
    <textarea
      className="w-full h-64 border rounded p-2 font-mono"
      value={value}
      placeholder={placeholder}
      onChange={handleChange}
    />
  )
}