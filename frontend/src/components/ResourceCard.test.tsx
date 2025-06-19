import { render, screen } from '@testing-library/react'
import ResourceCard from './ResourceCard'

describe('ResourceCard', () => {
  it('renders title, authors, and formatted date with correct link', () => {
    const props = {
      id: '123',
      title: 'Test Title',
      authors: ['Alice', 'Bob'],
      date: '2023-01-01',
    }
    render(<ResourceCard {...props} />)

    const link = screen.getByRole('link')
    expect(link).toHaveAttribute('href', `/resources/${props.id}`)

    expect(screen.getByText(props.title)).toBeInTheDocument()
    expect(screen.getByText(/Alice, Bob/)).toBeInTheDocument()
    expect(screen.getByText(/1\/1\/2023/)).toBeInTheDocument()
  })
})