export const dynamic = 'force-dynamic'
import Image from 'next/image'

import AboutCharts from '@/components/AboutCharts';


export const metadata = {
  title: 'About • Digital Library of Integral Ecology',
  description: 'Learn about our mission, architecture, data sources, and team.',
}

export default function AboutPage() {
  return (
    <div className="py-12 space-y-12 bg-slate-50 text-slate-800">
      <div className="container mx-auto p-4 md:p-8 max-w-7xl">

        <header className="text-center py-8 md:py-12">
          <h1 className="text-4xl md:text-6xl font-black text-[#F94144] tracking-tight">A New Ecosystem of Knowledge</h1>
          <p className="mt-4 text-lg md:text-xl text-[#577590] max-w-3xl mx-auto">Visualizing the future of the Integral Ecology Digital Library, a platform designed to connect ideas, data, and people in a dynamic, interconnected environment.</p>
        </header>

        <main className="space-y-16 md:space-y-24">

          <section id="audience" className="bg-white rounded-2xl shadow-lg p-6 md:p-10">
            <h2 className="text-3xl font-bold text-center text-[#F3722C] mb-2">Who is the Library For?</h2>
            <p className="text-center text-slate-600 mb-8 max-w-2xl mx-auto">This platform is designed as a convergence point for a diverse range of users, each with unique needs. The goal is to break down silos and foster cross-disciplinary understanding and collaboration.</p>
            <div className="chart-container">
              <canvas id="userGroupsChart"></canvas>
            </div>
          </section>

          <section id="core-engine">
            <h2 className="text-3xl font-bold text-center text-[#F8961E] mb-2">The Core Engine: Unifying Diverse Content</h2>
            <p className="text-center text-slate-600 mb-12 max-w-3xl mx-auto">At its heart, the library ingests multiple forms of media, standardizes them with rich, community-driven metadata, and makes them discoverable through a single, powerful search interface.</p>
            <div className="grid grid-cols-1 md:grid-cols-5 items-center gap-6 md:gap-4 text-center">
              <div className="flow-item p-4 rounded-xl">
                <span className="text-4xl">📄</span>
                <h3 className="font-bold mt-2">Texts</h3>
                <p className="text-sm text-slate-500">Articles & Books</p>
              </div>
              <div className="flow-arrow hidden md:block">&rarr;</div>
              <div className="flow-item p-4 rounded-xl">
                <span className="text-4xl">📊</span>
                <h3 className="font-bold mt-2">Data</h3>
                <p className="text-sm text-slate-500">Datasets & Stats</p>
              </div>
              <div className="flow-arrow block md:hidden mx-auto transform rotate-90 my-4">&rarr;</div>
              <div className="flow-item col-span-1 md:col-span-5 md:col-start-2 md:mt-8 p-6 rounded-2xl border-4 border-[#43AA8B]">
                <span className="text-5xl">🔎</span>
                <h3 className="text-2xl font-extrabold mt-2 text-[#43AA8B]">Unified Search & Tagging</h3>
                <p className="text-slate-600">One portal to access all knowledge</p>
              </div>
              <div className="flow-arrow block md:hidden mx-auto transform rotate-90 my-4">&rarr;</div>
              <div className="flow-item p-4 rounded-xl md:mt-0 mt-4">
                <span className="text-4xl">🎧</span>
                <h3 className="font-bold mt-2">Audio</h3>
                <p className="text-sm text-slate-500">Podcasts & Lectures</p>
              </div>
              <div className="flow-arrow hidden md:block">&larr;</div>
              <div className="flow-item p-4 rounded-xl">
                <span className="text-4xl">🎬</span>
                <h3 className="font-bold mt-2">Video</h3>
                <p className="text-sm text-slate-500">Films & Talks</p>
              </div>
            </div>
          </section>

          <section id="innovative-features" className="bg-white rounded-2xl shadow-lg p-6 md:p-10">
            <h2 className="text-3xl font-bold text-center text-[#90BE6D] mb-8">Pushing the Boundaries of Discovery</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
              <div className="flex flex-col">
                <h3 className="text-2xl font-bold text-[#43AA8B] mb-2">The "Ecology Explorer"</h3>
                <p className="text-slate-600 mb-6">Move beyond linear search results. The Ecology Explorer creates a visual, node-based web of knowledge, revealing hidden connections between different pieces of content and encouraging serendipitous discovery.</p>
                <div className="relative h-64 w-full bg-slate-100 rounded-xl p-4 flex-grow">
                  <div id="node-graph"></div>
                </div>
              </div>
              <div className="flex flex-col">
                <h3 className="text-2xl font-bold text-[#43AA8B] mb-2">Semantic & AI-Powered Search</h3>
                <p className="text-slate-600 mb-6">Our AI analyzes content for meaning, not just keywords. It understands concepts and context to deliver recommendations that are more relevant and insightful, connecting disparate fields of study.</p>
                <div className="bg-slate-100 rounded-xl p-4 flex-grow space-y-4">
                  <div>
                    <p className="font-semibold text-slate-500 text-sm">TRADITIONAL SEARCH FOR "WATER"</p>
                    <div className="bg-white p-2 mt-1 rounded-md shadow-sm">Returns: 1. Water Quality Reports 2. H₂O Chemical Formula</div>
                  </div>
                  <div>
                    <p className="font-semibold text-[#43AA8B] text-sm">AI SEMANTIC SEARCH FOR "WATER"</p>
                    <div className="bg-white p-2 mt-1 rounded-md shadow-sm">Also suggests: 1. Podcast on spiritual meaning of rivers 2. Indigenous water rights policy paper</div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section id="engagement">
            <h2 className="text-3xl font-bold text-center text-[#43AA8B] mb-2">Engaging Users, Building Community</h2>
            <p className="text-center text-slate-600 mb-12 max-w-3xl mx-auto">The library is a living platform, empowering users not just to consume information, but to analyze, curate, and discuss it. These tools turn passive readers into active participants.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 text-center">
              <div className="bg-white p-6 rounded-2xl shadow-lg">
                <div className="text-5xl mb-4">🌍</div>
                <h3 className="text-xl font-bold text-[#F94144]">Story of a Place</h3>
                <p className="text-slate-600 mt-2">Explore content through an interactive map. Discover scientific data, indigenous stories, and local reports tied to specific geographic locations, grounding global issues in local context.</p>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg">
                <div className="text-5xl mb-4">💬</div>
                <h3 className="text-xl font-bold text-[#F3722C]">Collaborative Annotation</h3>
                <p className="text-slate-600 mt-2">Highlight text and share insights directly on documents. Learn from the notes of experts and engage in conversations within the texts themselves, creating layers of community knowledge.</p>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg md:col-span-2 lg:col-span-1">
                <div className="text-5xl mb-4">📚</div>
                <h3 className="text-xl font-bold text-[#F8961E]">"Living Syllabi"</h3>
                <p className="text-slate-600 mt-2">Curate personal or public collections of library resources. Educators can build course packs, and research groups can create shared repositories for their projects, making knowledge organization seamless.</p>
              </div>
            </div>
          </section>

          <section id="map-section" className="bg-white rounded-2xl shadow-lg p-6 md:p-10">
            <h2 className="text-3xl font-bold text-center text-[#577590] mb-2">Geospatial Discovery: Story of a Place</h2>
            <p className="text-center text-slate-600 mb-8 max-w-2xl mx-auto">This interactive map allows users to explore the library's content geographically. Each point represents a location with a rich collection of connected resources—from scientific data to cultural narratives—demonstrating the core principle of integral ecology: everything is connected.</p>
            <div id="map-container" className="w-full h-[50vh] max-h-[600px] rounded-xl overflow-hidden"></div>
          </section>

        </main>

        <footer className="text-center py-10 mt-16 border-t border-slate-200">
          <p className="text-slate-500">Integral Ecology Digital Library Infographic</p>
          <p className="text-xs text-slate-400 mt-2">Visualizations created with Chart.js and Plotly.js. No SVG or Mermaid JS used in this infographic.</p>
        </footer>

        

      </div>

      
    </div>
  )
}