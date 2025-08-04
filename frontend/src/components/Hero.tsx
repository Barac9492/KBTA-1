'use client'

import Link from 'next/link'
import { ArrowRight, Play } from 'lucide-react'

export function Hero() {
  const showDemo = () => {
    const demoContent = `
      <div class="p-6 max-w-2xl">
        <h3 class="text-2xl font-bold text-pink-600 mb-4">Sample Daily Briefing</h3>
        <div class="space-y-4">
          <div class="bg-white/90 backdrop-blur-sm rounded-lg p-4 border border-pink-200">
            <h4 class="text-lg font-semibold text-purple-600 mb-2">🌸 Trending: Glass Skin Innovation</h4>
            <p class="text-gray-700">New formulations combining propolis and ceramides are dominating Korean beauty forums. Expect 40% increase in related product launches by Q2 2025.</p>
          </div>
          <div class="bg-white/90 backdrop-blur-sm rounded-lg p-4 border border-blue-200">
            <h4 class="text-lg font-semibold text-blue-600 mb-2">📊 Market Alert: Tariff Changes</h4>
            <p class="text-gray-700">US import duties on Korean cosmetics may increase by 15% starting March 2025. Consider alternative sourcing strategies.</p>
          </div>
        </div>
        <button onclick="this.parentElement.parentElement.remove()" class="mt-4 bg-pink-500 text-white px-4 py-2 rounded-lg hover:bg-pink-600 transition-colors">
          Close Demo
        </button>
      </div>
    `
    
    const modal = document.createElement('div')
    modal.className = 'fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50'
    modal.innerHTML = demoContent
    document.body.appendChild(modal)
    
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove()
    })
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('https://images.unsplash.com/photo-1556228720-195a672e8a03?w=1920&h=1080&fit=crop')`
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-pink-900/50 via-purple-900/50 to-rose-900/50"></div>
      </div>

      {/* Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-20 h-20 bg-pink-200/20 rounded-full blur-xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-purple-200/20 rounded-full blur-xl animate-pulse" style={{ animationDelay: '2s' }}></div>
        <div className="absolute bottom-20 left-1/3 w-12 h-12 bg-rose-200/20 rounded-full blur-xl animate-pulse" style={{ animationDelay: '4s' }}></div>
      </div>

      {/* Content */}
      <div className="relative z-10 text-center px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <div className="space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20">
            <span className="text-sm font-medium text-white">✨ The Bloomberg of Beauty</span>
          </div>

          {/* Main Heading */}
          <h1 className="text-5xl md:text-7xl font-bold text-white leading-tight">
            Discover Tomorrow&apos;s
            <br />
            <span className="bg-gradient-to-r from-pink-300 to-purple-300 bg-clip-text text-transparent">
              K-Beauty Trends
            </span>
            <br />
            Today
          </h1>

          {/* Description */}
          <p className="text-xl md:text-2xl text-white/90 max-w-3xl mx-auto leading-relaxed">
            AI-powered daily briefings, personalized insights, and market forecasts for beauty professionals and enthusiasts. 
            Your gateway to the future of K-beauty intelligence.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/subscribe"
              className="group inline-flex items-center px-8 py-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold rounded-full text-lg shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200"
            >
              Sign Up Free
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            
            <button
              onClick={showDemo}
              className="group inline-flex items-center px-8 py-4 bg-white/10 backdrop-blur-sm text-white font-semibold rounded-full text-lg border border-white/20 hover:bg-white/20 transition-all duration-200"
            >
              <Play className="mr-2 w-5 h-5" />
              View Demo
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-2">24/7</div>
              <div className="text-white/80">AI Monitoring</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-2">500+</div>
              <div className="text-white/80">Sources Analyzed</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-2">95%</div>
              <div className="text-white/80">Accuracy Rate</div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white/60 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </section>
  )
} 