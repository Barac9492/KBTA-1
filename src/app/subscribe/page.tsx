'use client';

import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Navigation } from '@/components/Navigation';
import { 
  Bell, 
  Mail, 
  Smartphone, 
  Calendar,
  CheckCircle,
  Sparkles
} from 'lucide-react';

export default function SubscribePage() {
  return (
    <Navigation>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Subscribe to Daily Briefings
              </h1>
              <p className="text-gray-600">
                Get daily K-beauty trend insights delivered to your inbox
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Bell className="w-6 h-6 text-pink-500" />
              <Badge variant="secondary" className="bg-pink-100 text-pink-800">
                Coming Soon
              </Badge>
            </div>
          </div>
        </div>

        {/* Subscription Options */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center mb-4">
                <Mail className="w-6 h-6 text-pink-600" />
              </div>
              <CardTitle className="text-xl">Email Digest</CardTitle>
              <p className="text-sm text-gray-600">
                Daily briefing summaries delivered to your inbox
              </p>
            </CardHeader>
            <CardContent className="text-center">
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Executive summary
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Top 3 trends
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Actionable insights
                </li>
              </ul>
              <Button className="w-full bg-pink-500 hover:bg-pink-600" disabled>
                Coming Soon
              </Button>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <Smartphone className="w-6 h-6 text-purple-600" />
              </div>
              <CardTitle className="text-xl">Mobile App</CardTitle>
              <p className="text-sm text-gray-600">
                Native mobile app with push notifications
              </p>
            </CardHeader>
            <CardContent className="text-center">
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Push notifications
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Offline access
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Interactive charts
                </li>
              </ul>
              <Button className="w-full bg-purple-500 hover:bg-purple-600" disabled>
                Coming Soon
              </Button>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <CardTitle className="text-xl">Weekly Report</CardTitle>
              <p className="text-sm text-gray-600">
                Comprehensive weekly analysis and forecasts
              </p>
            </CardHeader>
            <CardContent className="text-center">
              <ul className="space-y-2 text-sm text-gray-600 mb-6">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Market analysis
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Trend forecasts
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  Investment insights
                </li>
              </ul>
              <Button className="w-full bg-blue-500 hover:bg-blue-600" disabled>
                Coming Soon
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Features */}
        <Card className="border-0 shadow-lg bg-gradient-to-r from-pink-50 to-purple-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-xl">
              <Sparkles className="w-5 h-5 text-pink-600" />
              Why Subscribe?
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Stay Ahead of Trends</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Get early insights into emerging K-beauty trends before they become mainstream. 
                  Our AI-powered analysis identifies patterns and opportunities that traditional 
                  market research might miss.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Data-Driven Decisions</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Make informed business decisions with comprehensive trend analysis, 
                  market forecasts, and actionable recommendations backed by real-time 
                  data from multiple sources.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Save Time & Resources</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Skip hours of manual research and analysis. Our automated system 
                  processes thousands of data points daily to deliver concise, 
                  actionable insights directly to you.
                </p>
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-3">Expert Analysis</h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  Benefit from AI-powered analysis that combines market intelligence, 
                  consumer behavior patterns, and industry expertise to provide 
                  comprehensive trend insights.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </Navigation>
  );
} 