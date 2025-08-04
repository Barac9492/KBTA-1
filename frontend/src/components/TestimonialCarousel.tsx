'use client'

import { useState, useEffect } from 'react'
import { ChevronLeft, ChevronRight } from 'lucide-react'

const testimonials = [
  {
    id: 1,
    quote: "K-Beauty Trend Agent has revolutionized how I discover new products. The AI insights are spot-on and help me stay ahead of trends before they hit mainstream.",
    author: "Sarah Kim",
    role: "Beauty Influencer",
    handle: "@sarahkbeauty",
    avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face"
  },
  {
    id: 2,
    quote: "As a beauty marketer, this platform is invaluable. The predictive analytics help us launch products at the perfect time, and the market insights are gold.",
    author: "Michael Chen",
    role: "Marketing Director",
    company: "GlowCo",
    avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face"
  },
  {
    id: 3,
    quote: "The tariff and supply chain insights have saved us thousands. We can now source products strategically and avoid costly delays.",
    author: "Lisa Park",
    role: "Retail Manager",
    company: "BeautyMart",
    avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face"
  }
]

export function TestimonialCarousel() {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % testimonials.length)
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const goToSlide = (index: number) => {
    setCurrentIndex(index)
  }

  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + testimonials.length) % testimonials.length)
  }

  const goToNext = () => {
    setCurrentIndex((prev) => (prev + 1) % testimonials.length)
  }

  return (
    <div className="relative max-w-4xl mx-auto">
      {/* Testimonial */}
      <div className="relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-xl">
        <div className="flex transition-transform duration-500 ease-in-out" style={{ transform: `translateX(-${currentIndex * 100}%)` }}>
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="w-full flex-shrink-0 p-8 md:p-12">
              <div className="text-center">
                {/* Quote */}
                <div className="mb-8">
                  <svg className="w-12 h-12 text-pink-200 dark:text-pink-800 mx-auto mb-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                  </svg>
                  <p className="text-xl md:text-2xl text-gray-700 dark:text-gray-300 leading-relaxed italic">
                    "{testimonial.quote}"
                  </p>
                </div>

                {/* Author */}
                <div className="flex items-center justify-center space-x-4">
                  <img
                    src={testimonial.avatar}
                    alt={testimonial.author}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                  <div className="text-left">
                    <div className="font-semibold text-gray-900 dark:text-white">
                      {testimonial.author}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      {testimonial.role}
                      {testimonial.company && ` at ${testimonial.company}`}
                      {testimonial.handle && ` • ${testimonial.handle}`}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Buttons */}
      <button
        onClick={goToPrevious}
        className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white dark:bg-gray-800 rounded-full p-2 shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110"
        aria-label="Previous testimonial"
      >
        <ChevronLeft className="w-6 h-6 text-gray-600 dark:text-gray-400" />
      </button>

      <button
        onClick={goToNext}
        className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white dark:bg-gray-800 rounded-full p-2 shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110"
        aria-label="Next testimonial"
      >
        <ChevronRight className="w-6 h-6 text-gray-600 dark:text-gray-400" />
      </button>

      {/* Dots */}
      <div className="flex justify-center space-x-2 mt-8">
        {testimonials.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            className={`w-3 h-3 rounded-full transition-all duration-200 ${
              index === currentIndex
                ? 'bg-pink-500 scale-125'
                : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500'
            }`}
            aria-label={`Go to testimonial ${index + 1}`}
          />
        ))}
      </div>
    </div>
  )
} 