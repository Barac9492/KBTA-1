'use client'

import Link from 'next/link'
import { Check, Star } from 'lucide-react'

const plans = [
  {
    name: 'Free',
    price: '$0',
    period: 'Forever',
    description: 'Perfect for getting started with K-beauty insights',
    features: [
      'Basic trend insights',
      'Daily email digest',
      'Limited API calls',
      'Community access',
      'Basic personalization'
    ],
    cta: 'Get Started',
    href: '/subscribe',
    popular: false
  },
  {
    name: 'Premium',
    price: '$9',
    period: 'per month',
    description: 'For beauty professionals and enthusiasts',
    features: [
      'Full trend reports',
      'Advanced personalization',
      'Predictive analytics',
      'Priority support',
      'API access',
      'Export data',
      'Tariff alerts'
    ],
    cta: 'Start Free Trial',
    href: '/subscribe',
    popular: true
  },
  {
    name: 'Enterprise',
    price: '$29',
    period: 'per month',
    description: 'For teams and organizations',
    features: [
      'Everything in Premium',
      'Custom integrations',
      'Dedicated support',
      'White-label options',
      'Advanced forecasting',
      'Team collaboration',
      'Custom alerts'
    ],
    cta: 'Contact Sales',
    href: '/contact',
    popular: false
  }
]

export function PricingTable() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
      {plans.map((plan, index) => (
        <div
          key={index}
          className={`relative bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border-2 ${
            plan.popular
              ? 'border-pink-500 scale-105'
              : 'border-gray-100 dark:border-gray-700'
          }`}
        >
          {/* Popular Badge */}
          {plan.popular && (
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <div className="bg-gradient-to-r from-pink-500 to-purple-600 text-white px-4 py-2 rounded-full text-sm font-semibold flex items-center gap-2">
                <Star className="w-4 h-4" />
                Most Popular
              </div>
            </div>
          )}

          {/* Header */}
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              {plan.name}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {plan.description}
            </p>
            <div className="mb-6">
              <span className="text-4xl font-bold text-gray-900 dark:text-white">
                {plan.price}
              </span>
              <span className="text-gray-600 dark:text-gray-400 ml-2">
                {plan.period}
              </span>
            </div>
          </div>

          {/* Features */}
          <ul className="space-y-4 mb-8">
            {plan.features.map((feature, featureIndex) => (
              <li key={featureIndex} className="flex items-start gap-3">
                <Check className="w-5 h-5 text-pink-500 mt-0.5 flex-shrink-0" />
                <span className="text-gray-700 dark:text-gray-300">
                  {feature}
                </span>
              </li>
            ))}
          </ul>

          {/* CTA Button */}
          <Link
            href={plan.href}
            className={`block w-full text-center py-3 px-6 rounded-full font-semibold transition-all duration-200 ${
              plan.popular
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white hover:shadow-lg transform hover:-translate-y-1'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
          >
            {plan.cta}
          </Link>
        </div>
      ))}
    </div>
  )
} 