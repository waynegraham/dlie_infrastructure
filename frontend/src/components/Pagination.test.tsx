import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Pagination from './Pagination'

describe('Pagination', () => {
  it('does not render when totalPages <= 1', () => {
    const { container } = render(
      <Pagination
        currentPage={1}
        totalPages={1}
        pageSize={10}
        totalItems={10}
        onPageChange={() => {}}
      />
    )
    expect(container).toBeEmptyDOMElement()
  })

  it('renders pages and navigates correctly', async () => {
    const onPageChange = jest.fn()
    render(
      <Pagination
        currentPage={2}
        totalPages={3}
        pageSize={10}
        totalItems={30}
        onPageChange={onPageChange}
      />
    )

    await userEvent.click(screen.getByRole('button', { name: /prev/i }))
    expect(onPageChange).toHaveBeenCalledWith(1)

    await userEvent.click(screen.getByRole('button', { name: /next/i }))
    expect(onPageChange).toHaveBeenCalledWith(3)

    await userEvent.click(screen.getByRole('button', { name: '1' }))
    expect(onPageChange).toHaveBeenCalledWith(1)

    const current = screen.getByRole('button', { name: '2' })
    expect(current).toHaveClass('bg-teal-600')
  })

  it('disables navigation buttons on edges', () => {
    const onPageChange = jest.fn()
    render(
      <Pagination
        currentPage={1}
        totalPages={3}
        pageSize={10}
        totalItems={30}
        onPageChange={onPageChange}
      />
    )
    expect(screen.getByRole('button', { name: /prev/i })).toBeDisabled()
    expect(screen.getByRole('button', { name: /next/i })).toBeEnabled()

    render(
      <Pagination
        currentPage={3}
        totalPages={3}
        pageSize={10}
        totalItems={30}
        onPageChange={onPageChange}
      />
    )
    expect(screen.getByRole('button', { name: /next/i })).toBeDisabled()
  })
})