'use client'

interface FeatureCardProps {
  title: string
  description: string
  icon: string
  gradient: string
}

export function FeatureCard({ title, description, icon, gradient }: FeatureCardProps) {
  return (
    <div className="group relative bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transform hover:-translate-y-2 transition-all duration-300 border border-gray-100 dark:border-gray-700">
      {/* Gradient Border */}
      <div className={`absolute inset-0 rounded-2xl bg-gradient-to-r ${gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-300`}></div>
      
      {/* Icon */}
      <div className={`relative w-16 h-16 bg-gradient-to-r ${gradient} rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform duration-300`}>
        {icon}
      </div>

      {/* Content */}
      <div className="relative">
        <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 group-hover:text-pink-600 dark:group-hover:text-pink-400 transition-colors duration-300">
          {title}
        </h3>
        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
          {description}
        </p>
      </div>

      {/* Hover Effect */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-pink-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    </div>
  )
} 