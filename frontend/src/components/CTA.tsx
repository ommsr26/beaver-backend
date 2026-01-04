import Link from 'next/link'

export default function CTA() {
  return (
    <section className="py-20 bg-primary-600">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-white mb-4">
          Ready to Get Started?
        </h2>
        <p className="text-primary-100 mb-8 text-lg">
          Join thousands of developers using Beaver to access any AI model
        </p>
        <div className="flex justify-center gap-4">
          <Link
            href="/auth/register"
            className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition"
          >
            Get Started Free
          </Link>
          <Link
            href="/contact"
            className="bg-transparent text-white px-8 py-3 rounded-lg font-semibold border-2 border-white hover:bg-white hover:text-primary-600 transition"
          >
            Talk to Sales
          </Link>
        </div>
      </div>
    </section>
  )
}

