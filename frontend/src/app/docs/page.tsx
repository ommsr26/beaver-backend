export default function DocsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Documentation</h1>
        
        <div className="bg-white rounded-lg shadow p-8 space-y-8">
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Getting Started</h2>
            <p className="text-gray-600 mb-4">
              Beaver provides a unified API gateway to access any LLM model with a single API key.
            </p>
            <ol className="list-decimal list-inside space-y-2 text-gray-600">
              <li>Create an account and get your API key</li>
              <li>Top up your account balance</li>
              <li>Start making API calls to any model</li>
            </ol>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Authentication</h2>
            <p className="text-gray-600 mb-4">
              All API requests require authentication using a Bearer token:
            </p>
            <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto">
              <code>{`Authorization: Bearer beaver_your_api_key_here`}</code>
            </pre>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Chat Completion</h2>
            <p className="text-gray-600 mb-4">
              Make a chat completion request:
            </p>
            <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto">
              <code>{`POST /v1/models/{model_id}/chat
Authorization: Bearer beaver_your_api_key
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 512
}`}</code>
            </pre>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Available Models</h2>
            <p className="text-gray-600 mb-4">
              View all available models at <a href="/models" className="text-primary-600 hover:underline">/models</a>
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">API Reference</h2>
            <p className="text-gray-600 mb-4">
              Full API documentation is available at:
            </p>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:underline"
            >
              http://localhost:8000/docs
            </a>
          </section>
        </div>
      </div>
    </div>
  )
}

