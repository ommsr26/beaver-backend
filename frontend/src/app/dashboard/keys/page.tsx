'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { api } from '@/config/api'

export default function ApiKeysPage() {
  const [keys, setKeys] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [newKeyName, setNewKeyName] = useState('')
  const [creating, setCreating] = useState(false)
  const [newKey, setNewKey] = useState<string | null>(null)
  const router = useRouter()

  useEffect(() => {
    const apiKey = localStorage.getItem('beaver_api_key')
    if (!apiKey) {
      router.push('/auth/login')
      return
    }
    loadKeys()
  }, [router])

  const loadKeys = async () => {
    try {
      setLoading(true)
      const data = await api.listApiKeys()
      setKeys(data.api_keys || [])
    } catch (err: any) {
      console.error('Failed to load API keys', err)
      if (err.message?.includes('401') || err.message?.includes('403')) {
        router.push('/auth/login')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleCreateKey = async (e: React.FormEvent) => {
    e.preventDefault()
    setCreating(true)
    setNewKey(null)
    try {
      const data = await api.createApiKey(newKeyName || 'New Key')
      await loadKeys()
      setNewKeyName('')
      setNewKey(data.api_key)
    } catch (err: any) {
      alert(err.message || 'Failed to create API key')
    } finally {
      setCreating(false)
    }
  }

  const handleDeleteKey = async (keyId: string) => {
    if (!confirm('Are you sure you want to delete this API key? This action cannot be undone.')) {
      return
    }

    try {
      await api.deleteApiKey(keyId)
      await loadKeys()
    } catch (err: any) {
      alert(err.message || 'Failed to delete API key')
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    alert('API key copied to clipboard!')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <Link href="/dashboard" className="text-primary-600 hover:text-primary-700 mb-4 inline-block">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">API Keys</h1>
          <p className="text-gray-600 mt-2">
            Manage your API keys. Keep them secure and never share them publicly.
          </p>
        </div>

        {/* New Key Alert */}
        {newKey && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-green-900 mb-2">New API Key Created!</h3>
                <p className="text-sm text-green-700 mb-2">
                  Copy this key now - it won't be shown again:
                </p>
                <code className="block bg-white p-2 rounded border border-green-200 text-sm font-mono break-all">
                  {newKey}
                </code>
              </div>
              <button
                onClick={() => {
                  copyToClipboard(newKey)
                  setNewKey(null)
                }}
                className="ml-4 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
              >
                Copy
              </button>
            </div>
          </div>
        )}

        {/* Create New Key Form */}
        <div className="bg-white p-6 rounded-lg shadow mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New API Key</h2>
          <form onSubmit={handleCreateKey} className="flex gap-4">
            <input
              type="text"
              placeholder="Key name (e.g., Production, Development)"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
            <button
              type="submit"
              disabled={creating}
              className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 disabled:opacity-50"
            >
              {creating ? 'Creating...' : 'Create Key'}
            </button>
          </form>
        </div>

        {/* Keys List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Your API Keys</h2>
          </div>
          {keys.length === 0 ? (
            <div className="p-6 text-center text-gray-600">
              No API keys yet. Create your first one above.
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {keys.map((key) => (
                <div key={key.id} className="p-6 flex justify-between items-center">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-900">{key.name}</h3>
                      {key.is_active ? (
                        <span className="px-2 py-1 text-xs bg-green-100 text-green-700 rounded">
                          Active
                        </span>
                      ) : (
                        <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                          Inactive
                        </span>
                      )}
                    </div>
                    <code className="text-sm text-gray-600 font-mono">
                      {key.key_preview}
                    </code>
                    <div className="text-xs text-gray-500 mt-1">
                      Created: {new Date(key.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteKey(key.id)}
                    className="ml-4 text-red-600 hover:text-red-700 px-4 py-2 border border-red-200 rounded hover:bg-red-50"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

