'use client'

import { useEffect, useState } from 'react'
import { Hero } from '@/components/Hero'
import { FeatureCard } from '@/components/FeatureCard'
import { TestimonialCarousel } from '@/components/TestimonialCarousel'
import { PricingTable } from '@/components/PricingTable'
import { TrendCard } from '@/components/TrendCard'

interface Trend {
  id: string
  title: string
  summary: string
  category: string
  impact: string
}

const features = [
  {
    title: 'AI Daily Briefings',
    description: '24/7 automated scraping from top K-beauty sources including Glowpick, Olive Young, and social media trends with intelligent analysis.',
    icon: '🧠',
    gradient: 'from-pink-500 to-rose-500'
  },
  {
    title: 'Personalized Insights',
    description: 'Get recommendations tailored to your skin type, region, and specific beauty interests with our advanced AI personalization engine.',
    icon: '⚙️',
    gradient: 'from-purple-500 to-pink-500'
  },
  {
    title: 'Trend Forecasts',
    description: 'Predict upcoming trends like haircare booms, PDRN facials, propolis extracts, and climate-resilient skincare for 2025.',
    icon: '🔮',
    gradient: 'from-blue-500 to-purple-500'
  },
  {
    title: 'Tariff Alerts',
    description: 'Track tariff impacts, supply chain insights, and international market dynamics affecting K-beauty sourcing and pricing.',
    icon: '🌍',
    gradient: 'from-green-500 to-blue-500'
  }
]

const fallbackTrends: Trend[] = [
  {
    id: '1',
    title: 'Glass Skin Innovation',
    summary: 'New formulations combining propolis and ceramides are dominating Korean beauty forums. Expect 40% increase in related product launches.',
    category: 'Skincare',
    impact: 'High Impact'
  },
  {
    id: '2',
    title: 'Cream Makeup Revolution',
    summary: 'Cream-based makeup products are dominating the market with their natural, dewy finish. Sales up 60% in Q4 2024.',
    category: 'Makeup',
    impact: 'High Impact'
  },
  {
    id: '3',
    title: 'PDRN Facial Treatments',
    summary: 'Advanced overnight masks with PDRN and growth factors are revolutionizing skin repair. Trending across all age groups.',
    category: 'Skincare',
    impact: 'Medium Impact'
  }
]

export default function HomePage() {
  const [trends, setTrends] = useState<Trend[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const response = await fetch('/api/latest')
        const data = await response.json()
        
        if (data.status === 'success' && data.data?.trend_analysis?.trends) {
          const apiTrends = data.data.trend_analysis.trends.slice(0, 3).map((trend: { id?: string; title: string; summary: string; category: string }) => ({
            id: trend.id || Math.random().toString(),
            title: trend.title,
            summary: trend.summary,
            category: trend.category,
            impact: 'High Impact'
          }))
          setTrends(apiTrends)
        } else {
          setTrends(fallbackTrends)
        }
      } catch {
        console.log('Using fallback trends')
        setTrends(fallbackTrends)
      } finally {
        setLoading(false)
      }
    }

    fetchTrends()
  }, [])

  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <Hero />

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-6">
              Why Choose K-Beauty Trend Agent?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              The Bloomberg of Beauty - your gateway to the future of K-beauty intelligence
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <FeatureCard key={index} {...feature} />
            ))}
          </div>
        </div>
      </section>

      {/* Live Trends Section */}
      <section className="py-20 bg-gradient-to-r from-pink-50 to-purple-50 dark:from-gray-800 dark:to-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-6">
              Live Trend Preview
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Real-time insights from the world&apos;s most innovative beauty market
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {loading ? (
              // Loading skeletons
              Array.from({ length: 3 }).map((_, index) => (
                <div key={index} className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg animate-pulse">
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded mb-2"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded mb-2"></div>
                  <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3"></div>
                </div>
              ))
            ) : (
              trends.map((trend) => (
                <TrendCard key={trend.id} trend={trend} />
              ))
            )}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-6">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Join thousands of beauty professionals and enthusiasts who trust our insights
            </p>
          </div>
          
          <TestimonialCarousel />
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-gray-800 dark:to-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-6">
              Choose Your Plan
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Start free and scale as you grow. No hidden fees, cancel anytime.
            </p>
          </div>
          
          <PricingTable />
        </div>
      </section>
    </div>
  )
}
