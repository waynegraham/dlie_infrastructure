 'use client'
 
 import { useRouter, useParams } from 'next/navigation'
 import { useEffect, useState } from 'react'
 import MarkdownEditor from '@/components/MarkdownEditor'
 import ResourcePicker from '@/components/ResourcePicker'

 export default function EditExhibitPage() {
   const router = useRouter()
   const { slug } = useParams() as { slug: string }
   const [exhibit, setExhibit] = useState<{ title: string; markdown: string; resources: string[] } | null>(null)

   useEffect(() => {
     fetch(`/api/exhibits/${slug}`)
       .then(res => res.json())
       .then(data => setExhibit(data))
   }, [slug])

   if (!exhibit) return <p>Loading…</p>

   return (
     <div className="space-y-6">
       <h1 className="text-2xl font-bold">Edit Exhibit: {exhibit.title}</h1>

       <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
         <div>
           <label className="block mb-2 font-medium">Narrative</label>
           <MarkdownEditor
             initialValue={exhibit.markdown}
             onChange={value => setExhibit(prev => prev && { ...prev, markdown: value })}
           />
         </div>
         <div>
           <label className="block mb-2 font-medium">Resources</label>
           <ResourcePicker
             selected={exhibit.resources}
             onChange={selected => setExhibit(prev => prev && { ...prev, resources: selected })}
           />
         </div>
       </div>

       <button
         onClick={async () => {
           await fetch(`/api/exhibits/${slug}`, {
             method: 'PUT',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify(exhibit),
           })
           router.push(`/exhibits/${slug}`)
         }}
         className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700"
       >
         Save Changes
       </button>
     </div>
   )
 }