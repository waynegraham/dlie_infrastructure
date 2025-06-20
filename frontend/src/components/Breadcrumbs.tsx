'use client'

import Link from 'next/link'
import React from 'react'

export interface BreadcrumbItem {
  /** Label to display */
  label: string
  /** Href to link to (omitted for current page) */
  href?: string
}

export interface BreadcrumbsProps {
  /** Ordered list of breadcrumb items */
  items: BreadcrumbItem[]
}

/**
 * Simple breadcrumb navigation.
 * The last item is rendered as plain text (current page).
 */
export default function Breadcrumbs({ items }: BreadcrumbsProps) {
  if (!items || items.length === 0) {
    return null
  }
  return (
    <nav aria-label="Breadcrumb" className="text-sm text-gray-600">
      <ol className="flex items-center space-x-2">
        {items.map((item, idx) => {
          const isLast = idx === items.length - 1
          return (
            <li key={idx} className="flex items-center">
              {isLast || !item.href ? (
                <span aria-current="page">{item.label}</span>
              ) : (
                <Link href={item.href} className="hover:underline">
                  {item.label}
                </Link>
              )}
              {!isLast && <span className="mx-2">/</span>}
            </li>
          )
        })}
      </ol>
    </nav>
  )
}