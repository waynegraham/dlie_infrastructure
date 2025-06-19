// src/components/ResourcePicker.tsx
'use client'

import React from 'react'

export interface ResourcePickerProps {
  selected: string[]
  onChange: (selected: string[]) => void
}

export default function ResourcePicker({
  selected,
  onChange,
}: ResourcePickerProps) {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const options = Array.from(e.target.selectedOptions).map(o => o.value)
    onChange(options)
  }

  return (
    <select
      multiple
      value={selected}
      onChange={handleChange}
      className="w-full border rounded p-2"
      size={5}
    >
      {/* TODO: replace with dynamic list */}
      <option value="resource-1">Resource 1</option>
      <option value="resource-2">Resource 2</option>
      <option value="resource-3">Resource 3</option>
      <option value="resource-4">Resource 4</option>
      <option value="resource-5">Resource 5</option>
    </select>
  )
}