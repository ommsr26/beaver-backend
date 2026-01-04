'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { api } from '@/config/api'

export default function UsagePage() {
  const [usage, setUsage] = useState<any>(null)
  const [billing, setBilling] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(30)
  const router = useRouter()

  useEffect(() => {
    const apiKey = localStorage.getItem('beaver_api_key')
    if (!apiKey) {
      router.push('/auth/login')
      return
    }
    loadData()
  }, [router, days])

  const loadData = async () => {
    try {
      setLoading(true)
      const [usageData, billingData] = await Promise.all([
        api.getUsage(days),
        api.getBilling(50),
      ])
      setUsage(usageData)
      setBilling(billingData)
    } catch (err: any) {
      console.error('Failed to load usage data', err)
    } finally {
      setLoading(false)
    }
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
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <Link href="/dashboard" className="text-primary-600 hover:text-primary-700 mb-4 inline-block">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Usage Analytics</h1>
        </div>

        {/* Period Selector */}
        <div className="bg-white p-4 rounded-lg shadow mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Period
          </label>
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>

        {/* Summary Stats */}
        {usage && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm text-gray-600 mb-1">Total Requests</div>
              <div className="text-2xl font-bold text-gray-900">
                {usage.summary?.total_requests || 0}
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm text-gray-600 mb-1">Input Tokens</div>
              <div className="text-2xl font-bold text-gray-900">
                {usage.summary?.total_input_tokens?.toLocaleString() || 0}
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm text-gray-600 mb-1">Output Tokens</div>
              <div className="text-2xl font-bold text-gray-900">
                {usage.summary?.total_output_tokens?.toLocaleString() || 0}
              </div>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-sm text-gray-600 mb-1">Total Cost</div>
              <div className="text-2xl font-bold text-primary-600">
                ${usage.summary?.total_cost?.toFixed(4) || '0.0000'}
              </div>
            </div>
          </div>
        )}

        {/* Usage by Model */}
        {usage && usage.by_model && usage.by_model.length > 0 && (
          <div className="bg-white rounded-lg shadow mb-8">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Usage by Model</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Model</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Requests</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Input Tokens</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Output Tokens</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cost</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {usage.by_model.map((model: any, index: number) => (
                    <tr key={index}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {model.model_id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {model.requests}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {model.input_tokens.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {model.output_tokens.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        ${model.cost.toFixed(4)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Billing History */}
        {billing && billing.transactions && billing.transactions.length > 0 && (
          <div className="bg-white rounded-lg shadow">
            <div className="p-6 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-900">Billing History</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {billing.transactions.map((txn: any) => (
                <div key={txn.id} className="p-6 flex justify-between items-center">
                  <div>
                    <div className="font-medium text-gray-900">{txn.description}</div>
                    <div className="text-sm text-gray-500">
                      {new Date(txn.created_at).toLocaleString()}
                    </div>
                  </div>
                  <div className={`text-lg font-semibold ${
                    txn.amount >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {txn.amount >= 0 ? '+' : ''}${txn.amount.toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

