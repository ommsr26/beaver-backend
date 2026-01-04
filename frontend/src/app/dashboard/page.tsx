'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { api } from '@/config/api'

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null)
  const [balance, setBalance] = useState(0)
  const [usage, setUsage] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const apiKey = localStorage.getItem('beaver_api_key')
    if (!apiKey) {
      router.push('/auth/login')
      return
    }

    loadData()
  }, [router])

  const loadData = async () => {
    try {
      const [userData, balanceData, usageData] = await Promise.all([
        api.getCurrentUser(),
        api.getBalance(),
        api.getUsage(30).catch(() => null),
      ])
      setUser(userData)
      setBalance(balanceData.balance)
      setUsage(usageData)
    } catch (err) {
      console.error('Failed to load dashboard data', err)
      router.push('/auth/login')
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
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600 mb-1">Account Balance</div>
            <div className="text-3xl font-bold text-primary-600">
              ${balance.toFixed(2)}
            </div>
            <Link
              href="/dashboard/topup"
              className="text-sm text-primary-600 hover:text-primary-700 mt-2 inline-block"
            >
              Top Up →
            </Link>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600 mb-1">Total Requests</div>
            <div className="text-3xl font-bold text-gray-900">
              {usage?.summary?.total_requests || 0}
            </div>
            <div className="text-sm text-gray-500 mt-1">Last 30 days</div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <div className="text-sm text-gray-600 mb-1">Total Cost</div>
            <div className="text-3xl font-bold text-gray-900">
              ${usage?.summary?.total_cost?.toFixed(2) || '0.00'}
            </div>
            <div className="text-sm text-gray-500 mt-1">Last 30 days</div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Link
            href="/dashboard/keys"
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition"
          >
            <h3 className="font-semibold text-gray-900 mb-2">API Keys</h3>
            <p className="text-sm text-gray-600">
              Manage your API keys
            </p>
          </Link>

          <Link
            href="/playground"
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition"
          >
            <h3 className="font-semibold text-gray-900 mb-2">Playground</h3>
            <p className="text-sm text-gray-600">
              Test models in real-time
            </p>
          </Link>

          <Link
            href="/dashboard/usage"
            className="bg-white p-6 rounded-lg shadow hover:shadow-md transition"
          >
            <h3 className="font-semibold text-gray-900 mb-2">Usage Analytics</h3>
            <p className="text-sm text-gray-600">
              View detailed usage stats
            </p>
          </Link>
        </div>

        {/* Recent Activity */}
        {usage && usage.by_model && usage.by_model.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Usage by Model</h2>
            <div className="space-y-3">
              {usage.by_model.slice(0, 5).map((model: any, index: number) => (
                <div key={index} className="flex justify-between items-center py-2 border-b">
                  <div>
                    <div className="font-medium text-gray-900">{model.model_id}</div>
                    <div className="text-sm text-gray-600">
                      {model.requests} requests • ${model.cost.toFixed(4)} cost
                    </div>
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

