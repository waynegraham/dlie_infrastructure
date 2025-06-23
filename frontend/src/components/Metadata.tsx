// src/components/Metadata.tsx
'use client'

import React from 'react'
import Link from 'next/link'

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFilePdf } from "@fortawesome/free-solid-svg-icons";


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
        <strong>Provider:</strong> <Link href="/search/" className="text-teal-600 hover:underline">{provider}</Link>
      </p>
      {keywords && keywords.length > 0 && (
        <p>
          <strong>Keywords:</strong>{' '}
          {keywords.map((keyword, index) => (
            // Use React.Fragment to provide a key without adding extra DOM elements
            <React.Fragment key={keyword.id}>
              <Link
                href={`/search/?facet=${encodeURIComponent(keyword.display_name)}`}
                className="text-teal-600 hover:underline"
              >
                {keyword}
              </Link>
              {/* Add a comma and space if it's not the last item in the array */}
              {index < keywords.length - 1 && ', '}
            </React.Fragment>
          ))}
        </p>
      )}
      {/* {keywords.length > 0 && (
        <p>
          <strong>Keywords:</strong> {keywords.join(', ')}
        </p>
      )} */}
      {url && (
        <p>
          <FontAwesomeIcon icon={faFilePdf} />
          <strong>PDF:</strong>{' '}
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