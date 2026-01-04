'use client'

import { useState, useEffect } from 'react'
import { api } from '@/config/api'

interface Model {
  id: string
  display_name: string
  provider: string
  category: string
  pricing: {
    beaver_ai_input_price_per_1m: number
    beaver_ai_output_price_per_1m: number
  }
}

export default function Models() {
  const [models, setModels] = useState<Model[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadModels()
  }, [])

  const loadModels = async () => {
    try {
      setLoading(true)
      setError(null)
      const apiKey = localStorage.getItem('beaver_api_key')
      
      if (!apiKey) {
        // Try without auth (might work if endpoint allows)
        const data = await api.getModels()
        setModels(data.models || [])
      } else {
        const data = await api.getModels()
        setModels(data.models || [])
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load models')
      console.error('Error loading models:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Available Models</h2>
            <div className="text-gray-600">Loading models...</div>
          </div>
        </div>
      </section>
    )
  }

  if (error) {
    return (
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Available Models</h2>
            <div className="text-red-600 mb-4">{error}</div>
            <button
              onClick={loadModels}
              className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
            >
              Retry
            </button>
          </div>
        </div>
      </section>
    )
  }

  // Group models by provider
  const modelsByProvider = models.reduce((acc, model) => {
    if (!acc[model.provider]) {
      acc[model.provider] = []
    }
    acc[model.provider].push(model)
    return acc
  }, {} as Record<string, Model[]>)

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            {models.length}+ AI Models Available
          </h2>
          <p className="text-gray-600">
            Access models from OpenAI, Anthropic, Google, Deepseek, Perplexity, and Grok
          </p>
        </div>

        <div className="space-y-12">
          {Object.entries(modelsByProvider).map(([provider, providerModels]) => (
            <div key={provider}>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 capitalize">
                {provider} Models ({providerModels.length})
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {providerModels.map((model) => (
                  <div
                    key={model.id}
                    className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition"
                  >
                    <h4 className="font-semibold text-gray-900 mb-2">{model.display_name}</h4>
                    <p className="text-sm text-gray-600 mb-4">ID: {model.id}</p>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Input:</span>
                        <span className="font-medium">
                          ${model.pricing.beaver_ai_input_price_per_1m.toFixed(4)}/1M
                        </span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Output:</span>
                        <span className="font-medium">
                          ${model.pricing.beaver_ai_output_price_per_1m.toFixed(4)}/1M
                        </span>
                      </div>
                      <div className="mt-2">
                        <span className="inline-block px-2 py-1 text-xs bg-primary-100 text-primary-700 rounded">
                          {model.category}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

