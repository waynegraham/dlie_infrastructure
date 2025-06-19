import '@testing-library/jest-dom'
import React from 'react'

// Mock Next.js Link component for testing
jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ children, href, ...props }: { children: React.ReactNode; href?: string }) =>
    React.createElement('a', { href, ...props }, children),
}))

// Mock Next.js Image component for testing
jest.mock('next/image', () => ({
  __esModule: true,
  default: ({ src, alt, ...props }: { src: string; alt?: string }) =>
    React.createElement('img', { src, alt, ...props }),
}))