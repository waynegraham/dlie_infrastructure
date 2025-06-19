// src/app/about/page.tsx
import Image from 'next/image'

export const metadata = {
  title: 'About • Digital Ecology Library',
  description: 'Learn about our mission, architecture, data sources, and team.',
}

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-12 space-y-12">
      <h1 className="text-4xl font-extrabold text-center">About Digital Ecology Library</h1>

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
            <li><strong>Frontend:</strong> <a href="https://nextjs.org/">Next.js</a> & <a href="https://tailwindcss.com/">TailwindCSS</a></li>
            <li><strong>Auth:</strong> <a href="https://next-auth.js.org/">NextAuth.js</a> with Google OAuth</li>
            <li><strong>API:</strong> <a href="https://fastapi.tiangolo.com/">FastAPI</a> (Python)</li>
            <li><strong>Search:</strong> <a href="https://solr.apache.org/">Apache Solr</a></li>
            <li><strong>Database:</strong> <a href="https://www.postgresql.org/">PostgreSQL</a></li>
            <li><strong>Storage:</strong> <a href="https://aws.amazon.com/s3/">AWS S3</a> for media</li>
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
            <li>Resource API: <code><a href="http://localhost:8000/docs">http://localhost:8000/docs</a></code></li>
            <li>Solr Core: <code><a href="http://localhost:8983/solr/#/ecology/core-overview">ecology</a></code></li>
            <li>S3 Bucket: <code>digital-ecology-media</code></li>
            <li>RabbitMQ <code><a href="http://localhost:15672/">http://localhost:15672/</a></code> (guest/guest)</li>
            <li>Prometheus: <code><a href="http://localhost:9090/query">Prometheus</a></code></li>
            <li>Grafana: <code><a href="http://localhost:4000/">http://localhost:4000/</a></code> (admin/admin)</li>
            <li>cAdvisor: <code><a href="http://localhost:8081/containers/">http://localhost:8081/containers/</a></code></li>
            <li>External feeds & imports from partner repositories</li>
          </ul>
        </section>

        {/* Team */}
        <section className="p-6 bg-white rounded-2xl shadow-sm prose max-w-none">
          <h2>Our Team</h2>
          <ul>
            <li><strong>Alice Smith</strong> &ndash; Project Lead</li>
            <li><strong>Bob Johnson</strong> &ndash; Backend Engineer</li>
            <li><strong>Carol Lee</strong> &ndash; Frontend & UX Designer</li>
            <li><strong>Daniel Kim</strong> &ndash; DevOps & Monitoring</li>
          </ul>
        </section>
      </div>
    </div>
)
}