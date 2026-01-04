'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { api } from '@/config/api'

export default function Hero() {
  const [stats, setStats] = useState({
    modelCount: 31,
    uptime: '99.9%',
    latency: '50ms'
  })

  useEffect(() => {
    // Get model count
    const apiKey = localStorage.getItem('beaver_api_key')
    if (apiKey) {
      api.getModels()
        .then(data => setStats(prev => ({ ...prev, modelCount: data.total })))
        .catch(() => {})
    } else {
      // Try to get models anyway (might work if endpoint allows)
      api.getModels()
        .then(data => setStats(prev => ({ ...prev, modelCount: data.total })))
        .catch(() => {})
    }

    // Get uptime (public endpoint)
    api.getUptime()
      .then(data => setStats(prev => ({ ...prev, uptime: `${data.uptime_percentage}%` })))
      .catch(() => {})

    // Get latency (public endpoint)
    api.getLatency()
      .then(data => setStats(prev => ({ ...prev, latency: `${data.average_latency_ms}ms` })))
      .catch(() => {})
  }, [])

  return (
    <section className="bg-gradient-to-br from-primary-50 to-primary-100 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Unified API Gateway
            <br />
            <span className="text-primary-600">for Any LLM</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Access OpenAI, Anthropic, Google, Deepseek, Perplexity, and Grok models
            with a single API key. No need to manage multiple provider accounts.
          </p>

          {/* Stats */}
          <div className="flex justify-center gap-8 mb-12 flex-wrap">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">{stats.modelCount}+</div>
              <div className="text-sm text-gray-600">Models</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">{stats.uptime}</div>
              <div className="text-sm text-gray-600">Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary-600">{stats.latency}</div>
              <div className="text-sm text-gray-600">Avg Latency</div>
            </div>
          </div>

          {/* CTA Buttons */}
          <div className="flex justify-center gap-4">
            <Link
              href="/auth/register"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition"
            >
              Get Started
            </Link>
            <Link
              href="/docs"
              className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold border-2 border-primary-600 hover:bg-primary-50 transition"
            >
              View Documentation
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}

