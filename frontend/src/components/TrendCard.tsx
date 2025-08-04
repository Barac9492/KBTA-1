'use client'

interface Trend {
  id: string
  title: string
  summary: string
  category: string
  impact: string
}

interface TrendCardProps {
  trend: Trend
}

export function TrendCard({ trend }: TrendCardProps) {
  return (
    <div className="group bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300 border border-gray-100 dark:border-gray-700">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2 group-hover:text-pink-600 dark:group-hover:text-pink-400 transition-colors duration-300">
            {trend.title}
          </h4>
          <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
            {trend.summary}
          </p>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-700">
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-pink-100 dark:bg-pink-900/30 text-pink-800 dark:text-pink-200">
          {trend.category}
        </span>
        <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
          {trend.impact}
        </span>
      </div>

      {/* Hover Effect */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-pink-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    </div>
  )
} 