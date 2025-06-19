export const dynamic = 'force-dynamic'
import Image from 'next/image'

export const metadata = {
  title: 'About • Digital Library of Integral Ecology',
  description: 'Learn about our mission, architecture, data sources, and team.',
}

export default function AboutPage() {
  return (
    <div className="py-12 space-y-12">
      <h1 className="text-4xl font-extrabold text-center">About Digital Library of Integral Ecology</h1>

      <div className="grid gap-8 md:grid-cols-2">
        {/* Mission */}
        <section className="p-6 bg-white rounded-2xl shadow-sm prose max-w-none">
          <h2>Our Mission</h2>
          <p>
            We exist to curate and surface foundational resources on Integral Ecology—
            bringing together scholarship, policy analysis, and multimedia into one
            searchable, discoverable platform. Our goal is to empower scholars and
            policy-makers with the knowledge they need to address complex socio-ecological challenges.
          </p>
        </section>

        {/* Architecture */}
        <section className="p-6 bg-white rounded-2xl shadow-sm space-y-4">
          <h2 className="text-2xl font-semibold">Technical Architecture</h2>
          <p className="prose max-w-none">
            Our stack leverages modern, scalable technologies to deliver fast, rich
            discovery and curation experiences:
          </p>
          <ul className="list-disc list-inside prose max-w-none">
            <li><strong>Frontend:</strong> Next.js &amp; TailwindCSS</li>
            <li><strong>Auth:</strong> NextAuth.js with Google OAuth</li>
            <li><strong>API:</strong> FastAPI (Python)</li>
            <li><strong>Search:</strong> Apache Solr</li>
            <li><strong>Database:</strong> PostgreSQL</li>
            <li><strong>Storage:</strong> AWS S3 for media</li>
            <li><strong>Monitoring:</strong> Prometheus, Grafana, cAdvisor, Loki</li>
          </ul>
          <div className="relative w-full h-64 overflow-hidden rounded-lg">
            <Image
              src="/architecture-diagram.svg"
              alt="Architecture diagram"
              fill
              style={{ objectFit: 'contain' }}
              priority
            />
          </div>
        </section>

        {/* Data Sources */}
        <section className="p-6 bg-white rounded-2xl shadow-sm prose max-w-none">
          <h2>Data Sources</h2>
          <ul>
            <li>Resource API: <code>http://localhost:8000</code></li>
            <li>Solr Core: <code>ecology</code></li>
            <li>S3 Bucket: <code>digital-ecology-media</code></li>
            <li>External feeds &amp; imports from partner repositories</li>
          </ul>
        </section>

        {/* Team */}
        <section className="p-6 bg-white rounded-2xl shadow-sm prose max-w-none">
          <h2>Our Team</h2>
          <ul>
            <li><strong>Alice Smith</strong> &ndash; Project Lead</li>
            <li><strong>Bob Johnson</strong> &ndash; Backend Engineer</li>
            <li><strong>Carol Lee</strong> &ndash; Frontend &amp; UX Designer</li>
            <li><strong>Daniel Kim</strong> &ndash; DevOps &amp; Monitoring</li>
          </ul>
        </section>
      </div>
    </div>
  )
}