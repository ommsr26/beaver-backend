'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/config/api'

interface Message {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export default function PlaygroundPage() {
  const [models, setModels] = useState<any[]>([])
  const [selectedModel, setSelectedModel] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    const apiKey = localStorage.getItem('beaver_api_key')
    if (!apiKey) {
      router.push('/auth/login')
      return
    }

    loadModels()
  }, [router])

  const loadModels = async () => {
    try {
      const data = await api.getModels()
      setModels(data.models || [])
      if (data.models?.length > 0) {
        setSelectedModel(data.models[0].id)
      }
    } catch (err: any) {
      console.error('Failed to load models', err)
      setError('Failed to load models. Please check your API key.')
    }
  }

  const handleSend = async () => {
    if (!input.trim() || !selectedModel || loading) return

    const userMessage: Message = { role: 'user', content: input }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    setError(null)
    setLoading(true)

    try {
      const response = await api.chat(selectedModel, newMessages)
      const assistantMessage: Message = response.choices[0].message
      setMessages([...newMessages, assistantMessage])
    } catch (err: any) {
      setError(err.message || 'Failed to send message')
      console.error('Chat error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Chat Playground</h1>

        {/* Model Selector */}
        <div className="bg-white p-4 rounded-lg shadow mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Model
          </label>
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {models.map((model) => (
              <option key={model.id} value={model.id}>
                {model.display_name} ({model.provider}) - {model.category}
              </option>
            ))}
          </select>
        </div>

        {/* Chat Messages */}
        <div className="bg-white rounded-lg shadow mb-4 h-96 overflow-y-auto p-6">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 mt-20">
              Start a conversation by typing a message below
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-3xl rounded-lg p-4 ${
                      msg.role === 'user'
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <div className="text-xs font-semibold mb-1 opacity-75">
                      {msg.role === 'user' ? 'You' : 'Assistant'}
                    </div>
                    <div className="whitespace-pre-wrap">{msg.content}</div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg p-4">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Chat Input */}
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex gap-4">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              rows={3}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none"
            />
            <button
              onClick={handleSend}
              disabled={loading || !input.trim() || !selectedModel}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Sending...' : 'Send'}
            </button>
          </div>
          <div className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  )
}

