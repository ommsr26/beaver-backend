export default function FlowDiagram() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h2>
          <p className="text-gray-600">
            Simple integration, powerful results
          </p>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-center gap-8">
          {/* Step 1 */}
          <div className="text-center max-w-xs">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">1</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Get Your API Key</h3>
            <p className="text-gray-600 text-sm">
              Sign up and get your unified API key in seconds
            </p>
          </div>

          <div className="hidden md:block text-primary-600 text-2xl">→</div>

          {/* Step 2 */}
          <div className="text-center max-w-xs">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">2</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Top Up Balance</h3>
            <p className="text-gray-600 text-sm">
              Add funds to your account once, use across all models
            </p>
          </div>

          <div className="hidden md:block text-primary-600 text-2xl">→</div>

          {/* Step 3 */}
          <div className="text-center max-w-xs">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-2xl font-bold text-primary-600">3</span>
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Start Building</h3>
            <p className="text-gray-600 text-sm">
              Use any model with one API key. Balance auto-deducts.
            </p>
          </div>
        </div>

        {/* Code Example */}
        <div className="mt-12 max-w-2xl mx-auto">
          <div className="bg-gray-900 rounded-lg p-6 overflow-x-auto">
            <pre className="text-green-400 text-sm">
              <code>{`// Example: Chat with any model
const response = await fetch(
  'http://localhost:8000/v1/models/gpt-4o-mini/chat',
  {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer beaver_your_api_key',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [
        { role: 'user', content: 'Hello!' }
      ]
    })
  }
);`}</code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  )
}

