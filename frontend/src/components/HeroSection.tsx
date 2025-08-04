'use client';

import { motion } from 'framer-motion';
import { Sparkles, TrendingUp, Globe, Zap } from 'lucide-react';

interface HeroSectionProps {
  briefingCount: number;
  lastUpdated: string;
}

export function HeroSection({ briefingCount, lastUpdated }: HeroSectionProps) {
  return (
    <div className="relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-10 left-10 w-20 h-20 bg-pink-200/30 rounded-full blur-xl float-animation"></div>
        <div className="absolute top-20 right-20 w-16 h-16 bg-purple-200/30 rounded-full blur-xl float-animation" style={{ animationDelay: '2s' }}></div>
        <div className="absolute bottom-10 left-1/4 w-12 h-12 bg-rose-200/30 rounded-full blur-xl float-animation" style={{ animationDelay: '4s' }}></div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="glass-card p-8 rounded-2xl"
      >
        <div className="flex items-center justify-between mb-6">
          <div className="flex-1">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="flex items-center gap-3 mb-4"
            >
              <div className="w-12 h-12 bg-kbeauty-gradient rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold gradient-text mb-2">
                  🌸 K-Beauty Trend Briefing
                </h1>
                <p className="text-gray-600 text-lg">
                  AI-powered insights from the world&apos;s most innovative beauty market
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6"
            >
              <div className="flex items-center gap-3 p-4 bg-white/50 rounded-lg border border-pink-100">
                <TrendingUp className="w-5 h-5 text-pink-500" />
                <div>
                  <p className="text-sm text-gray-600">Latest Insights</p>
                  <p className="font-semibold text-gray-900">{briefingCount} sources analyzed</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3 p-4 bg-white/50 rounded-lg border border-purple-100">
                <Globe className="w-5 h-5 text-purple-500" />
                <div>
                  <p className="text-sm text-gray-600">Korean Market</p>
                  <p className="font-semibold text-gray-900">Real-time trends</p>
                </div>
              </div>
              
              <div className="flex items-center gap-3 p-4 bg-white/50 rounded-lg border border-rose-100">
                <Zap className="w-5 h-5 text-rose-500" />
                <div>
                  <p className="text-sm text-gray-600">Updated</p>
                  <p className="font-semibold text-gray-900">{lastUpdated}</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Cultural elements */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="flex items-center justify-between text-sm text-gray-500"
        >
          <div className="flex items-center gap-2">
            <span>🇰🇷</span>
            <span>Korean Beauty Intelligence</span>
          </div>
          <div className="flex items-center gap-2">
            <span>✨</span>
            <span>Glass Skin Technology</span>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
} 