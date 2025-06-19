// src/components/Metadata.tsx
'use client'

import React from 'react'

export interface MetadataProps {
  authors: string[]
  date: string
  doi?: string
  provider: string
  keywords: string[]
  url?: string
}

export default function Metadata({
  authors,
  date,
  doi,
  provider,
  keywords,
  url,
}: MetadataProps) {
  return (
    <div className="space-y-2 text-sm text-gray-700">
      <p>
        <strong>Authors:</strong> {authors.join(', ')}
      </p>
      <p>
        <strong>Date:</strong> {new Date(date).toLocaleDateString()}
      </p>
      {doi && (
        <p>
          <strong>DOI:</strong>{' '}
          <a
            href={`https://doi.org/${doi}`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-teal-600 hover:underline"
          >
            {doi}
          </a>
        </p>
      )}
      <p>
        <strong>Provider:</strong> {provider}
      </p>
      {keywords.length > 0 && (
        <p>
          <strong>Keywords:</strong> {keywords.join(', ')}
        </p>
      )}
      {url && (
        <p>
          <strong>Link:</strong>{' '}
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-teal-600 hover:underline"
          >
            View resource
          </a>
        </p>
      )}
    </div>
  )
}