import { render, screen } from '@testing-library/react'
import ExhibitCard from './ExhibitCard'

describe('ExhibitCard', () => {
  const baseProps = {
    title: 'Exhibit Title',
    excerpt: 'An excerpt',
    slug: 'exhibit-slug',
    thumbnailUrl: 'https://example.com/thumb.jpg',
  }

  it('renders link, title, excerpt, and an image when thumbnailUrl is provided', () => {
    render(<ExhibitCard {...baseProps} />)

    const link = screen.getByRole('link')
    expect(link).toHaveAttribute('href', `/exhibits/${baseProps.slug}`)

    expect(screen.getByText(baseProps.title)).toBeInTheDocument()
    expect(screen.getByText(baseProps.excerpt)).toBeInTheDocument()

    const img = screen.getByRole('img')
    expect(img).toHaveAttribute('src', baseProps.thumbnailUrl)
    expect(img).toHaveAttribute('alt', `Thumbnail for ${baseProps.title}`)
  })

  it('does not render an image when thumbnailUrl is undefined', () => {
    render(<ExhibitCard {...baseProps} thumbnailUrl={undefined} />)
    expect(screen.queryByRole('img')).toBeNull()
  })
})