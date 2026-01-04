export default function Features() {
  const features = [
    {
      title: 'Unified API',
      description: 'Access multiple LLM providers with a single API key. No need to manage multiple accounts.',
      icon: '🔑',
    },
    {
      title: 'Dynamic Pricing',
      description: 'Smart pricing based on model tiers. 3-12% cheaper than fixed markup systems.',
      icon: '💰',
    },
    {
      title: '31+ Models',
      description: 'Access models from OpenAI, Anthropic, Google, Deepseek, Perplexity, and Grok.',
      icon: '🤖',
    },
    {
      title: 'Automatic Billing',
      description: 'Balance automatically deducted per request. Transparent pricing with usage tracking.',
      icon: '💳',
    },
    {
      title: 'Rate Limiting',
      description: 'Built-in rate limiting and usage tracking to prevent abuse and ensure fair usage.',
      icon: '⚡',
    },
    {
      title: 'Easy Integration',
      description: 'Simple REST API compatible with OpenAI format. Works with existing code.',
      icon: '🔌',
    },
  ]

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose Beaver?</h2>
          <p className="text-gray-600">
            Everything you need to access any AI model with one API key
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

