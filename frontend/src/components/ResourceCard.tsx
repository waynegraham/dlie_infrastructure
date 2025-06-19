// src/components/ResourceCard.tsx
'use client'

import React from 'react'
import Link from 'next/link'

export interface ResourceCardProps {
  id: string
  title: string
  authors: string[]
  date: string
}

export default function ResourceCard({
  id,
  title,
  authors,
  date,
}: ResourceCardProps) {
  return (
    <Link
      href={`/resources/${id}`}
      className="block border rounded-lg p-4 hover:shadow-lg transition">

      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="text-sm text-gray-600">
        {authors.join(', ')} —{' '}
        {new Date(date).toLocaleDateString('en-US')}
      </p>

    </Link>
  );
}