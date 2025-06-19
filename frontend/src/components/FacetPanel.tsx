'use client'

import React from 'react'

export interface FacetOption {
  label: string;
  value: string;
  count: number;
}

export interface FacetPanelProps {
  facets: Record<string, FacetOption[]>;
  selected: Record<string, string[]>;
  onFacetChange: (category: string, selectedValues: string[]) => void;
}

export default function FacetPanel({ facets, selected, onFacetChange }: FacetPanelProps) {
  const handleToggle = (category: string, value: string) => {
    const current = selected[category] || [];
    const next = current.includes(value)
      ? current.filter(v => v !== value)
      : [...current, value];
    onFacetChange(category, next);
  };

  return (
    <aside className="bg-white p-4 border rounded shadow space-y-6">
      {Object.entries(facets).map(([category, options]) => (
        <div key={category} className="space-y-2">
          <h3 className="font-medium text-gray-800 capitalize">{category}</h3>
          <ul className="space-y-1">
            {options.map(opt => (
              <li key={opt.value}>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={selected[category]?.includes(opt.value) || false}
                    onChange={() => handleToggle(category, opt.value)}
                    className="mr-2"
                  />
                  <span className="flex justify-between w-full">
                    <span>{opt.label}</span>
                    <span className="text-sm text-gray-500">{opt.count}</span>
                  </span>
                </label>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </aside>
  )
}