// src/components/FullTextViewer.tsx
'use client'

import React from 'react'

export interface FullTextViewerProps {
  text: string
}

export default function FullTextViewer({ text }: FullTextViewerProps) {
  return (
    <div className="prose max-w-none whitespace-pre-wrap">
      {text}
    </div>
  )
}