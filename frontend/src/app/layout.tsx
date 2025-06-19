import './globals.css'
import ClientLayout from '@/components/ClientLayout'

export const metadata = {
  title: 'Digital Library of Integral Ecology',
  description: 'Discover and explore Integral Ecology resources',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col">
        {/* Client‐only wrapper here */}
        <ClientLayout>
          <main className="flex-grow container mx-auto px-4 py-6">
            {children}
          </main>
        </ClientLayout>
      </body>
    </html>
  )
}