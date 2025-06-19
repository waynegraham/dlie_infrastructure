// src/components/ExhibitCard.tsx
'use client'

import React from 'react'
import Link from 'next/link'
import Image from 'next/image'

export interface ExhibitCardProps {
  title: string
  excerpt: string
  thumbnailUrl?: string
  slug: string
}

export default function ExhibitCard({
  title,
  excerpt,
  thumbnailUrl,
  slug,
}: ExhibitCardProps) {
  return (
    <Link href={`/exhibits/${slug}`}>
      <a className="block border rounded-lg overflow-hidden hover:shadow-lg transition">
        {thumbnailUrl && (
          <Image
            src={thumbnailUrl}
            alt={`Thumbnail for ${title}`}
            width={400}
            height={160}
            className="w-full h-40 object-cover"
            priority={false}
          />
        )}
        <div className="p-4">
          <h3 className="text-lg font-semibold">{title}</h3>
          <p className="text-sm text-gray-600 mt-1">{excerpt}</p>
        </div>
      </a>
    </Link>
  )
}