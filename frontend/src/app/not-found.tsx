
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex h-screen items-center justify-center bg-gray-50 p-4">
      <div className="max-w-md text-center space-y-6">
        <h1 className="text-6xl font-extrabold">404</h1>
        <p className="text-xl text-gray-700">
          Oops! The page you’re looking for doesn’t exist.
        </p>
        <Link
          href="/"
          className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700"
        >
          Go back home
        </Link>
      </div>
    </div>
  )
}