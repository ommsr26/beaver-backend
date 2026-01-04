import Hero from '@/components/Hero'
import FlowDiagram from '@/components/FlowDiagram'
import Features from '@/components/Features'
import Models from '@/components/Models'
import CTA from '@/components/CTA'

export default function Home() {
  return (
    <div className="min-h-screen">
      <Hero />
      <FlowDiagram />
      <Features />
      <Models />
      <CTA />
    </div>
  )
}

