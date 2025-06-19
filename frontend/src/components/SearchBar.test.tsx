import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import SearchBar from './SearchBar'

describe('SearchBar', () => {
  it('renders with initialQuery and calls onSearch with trimmed value on button click', async () => {
    const onSearch = jest.fn()
    render(<SearchBar initialQuery="foo" onSearch={onSearch} />)

    const input = screen.getByRole('textbox', { name: /search query/i })
    expect(input).toHaveValue('foo')

    await userEvent.clear(input)
    await userEvent.type(input, '  bar  ')
    await userEvent.click(screen.getByRole('button', { name: /search/i }))
    expect(onSearch).toHaveBeenCalledWith('bar')
  })

  it('calls onSearch when Enter key is pressed', async () => {
    const onSearch = jest.fn()
    render(<SearchBar onSearch={onSearch} />)

    const input = screen.getByRole('textbox', { name: /search query/i })
    await userEvent.type(input, 'baz{enter}')
    expect(onSearch).toHaveBeenCalledWith('baz')
  })
})