'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { api } from '@/config/api'

export default function Navigation() {
  const [balance, setBalance] = useState(0)
  const [user, setUser] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [showMenu, setShowMenu] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const apiKey = localStorage.getItem('beaver_api_key')
    if (apiKey) {
      Promise.all([
        api.getBalance()
          .then(data => setBalance(data.balance))
          .catch(() => {}),
        api.getCurrentUser()
          .then(data => setUser(data))
          .catch(() => {})
      ]).finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const handleSignIn = () => {
    router.push('/auth/login')
  }

  const handleGetApiKey = () => {
    router.push('/dashboard/keys')
  }

  const handleLogout = async () => {
    await api.logout()
    setUser(null)
    setBalance(0)
    router.push('/')
  }

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <span className="text-2xl font-bold text-primary-600">🦫 Beaver</span>
          </Link>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/models" className="text-gray-700 hover:text-primary-600">
              Models
            </Link>
            <Link href="/playground" className="text-gray-700 hover:text-primary-600">
              Playground
            </Link>
            <Link href="/docs" className="text-gray-700 hover:text-primary-600">
              Docs
            </Link>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {loading ? (
              <div className="text-gray-500">Loading...</div>
            ) : user ? (
              <div className="flex items-center space-x-4">
                {/* Balance Display */}
                <div className="hidden sm:block text-sm">
                  <span className="text-gray-600">Balance: </span>
                  <span className="font-semibold text-primary-600">
                    ${balance.toFixed(2)}
                  </span>
                </div>

                {/* User Menu */}
                <div className="relative">
                  <button
                    onClick={() => setShowMenu(!showMenu)}
                    className="flex items-center space-x-2 text-gray-700 hover:text-primary-600"
                  >
                    <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                      <span className="text-primary-600 font-semibold">
                        {user.email?.[0]?.toUpperCase() || 'U'}
                      </span>
                    </div>
                    <span className="hidden sm:block">{user.email}</span>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  {showMenu && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                      <Link
                        href="/dashboard"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setShowMenu(false)}
                      >
                        Dashboard
                      </Link>
                      <Link
                        href="/dashboard/keys"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setShowMenu(false)}
                      >
                        API Keys
                      </Link>
                      <Link
                        href="/dashboard/usage"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        onClick={() => setShowMenu(false)}
                      >
                        Usage
                      </Link>
                      <button
                        onClick={() => {
                          handleLogout()
                          setShowMenu(false)
                        }}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Sign Out
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <>
                <button
                  onClick={handleSignIn}
                  className="text-gray-700 hover:text-primary-600 px-4 py-2"
                >
                  Sign In
                </button>
                <button
                  onClick={handleGetApiKey}
                  className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
                >
                  Get API Key
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

