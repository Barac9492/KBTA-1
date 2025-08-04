'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Navigation } from '@/components/Navigation';
import { TrendCard } from '@/components/TrendCard';
import { apiClient } from '@/lib/api';
import { DailyBriefing } from '@/lib/types';
import { 
  Download, 
  FileText, 
  TrendingUp, 
  Calendar,
  RefreshCw,
  AlertCircle,
  CheckCircle,
  Clock,
  BarChart3
} from 'lucide-react';

export default function Dashboard() {
  const [briefing, setBriefing] = useState<DailyBriefing | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState<string | null>(null);

  useEffect(() => {
    loadLatestBriefing();
  }, []);

  const loadLatestBriefing = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getLatestBriefing();
      if (response.success && response.data) {
        setBriefing(response.data);
      } else {
        setError(response.error || 'Failed to load briefing');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (type: 'markdown' | 'json') => {
    if (!briefing) return;
    
    setDownloading(type);
    try {
      const response = type === 'markdown' 
        ? await apiClient.downloadMarkdown(briefing.briefing_id)
        : await apiClient.downloadJson(briefing.briefing_id);
      
      if (response.success && response.data) {
        const url = window.URL.createObjectURL(response.data);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kbeauty-briefing-${briefing.briefing_id}.${type}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        setError(`Failed to download ${type} file`);
      }
    } catch (err) {
      setError(`Failed to download ${type} file`);
    } finally {
      setDownloading(null);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 text-pink-500 animate-spin mx-auto mb-4" />
            <p className="text-gray-600">Loading latest briefing...</p>
          </div>
        </div>
      </Navigation>
    );
  }

  if (error) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Briefing</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={loadLatestBriefing} className="bg-pink-500 hover:bg-pink-600">
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again
            </Button>
          </div>
        </div>
      </Navigation>
    );
  }

  if (!briefing) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <FileText className="w-8 h-8 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Briefing Available</h3>
            <p className="text-gray-600">No briefing has been generated yet.</p>
          </div>
        </div>
      </Navigation>
    );
  }

  return (
    <Navigation>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Daily K-Beauty Trend Briefing
              </h1>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  {formatDate(briefing.date)}
                </div>
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4" />
                  {briefing.trend_analysis.trends.length} trends analyzed
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  {briefing.scraped_posts_count} sources scraped
                </div>
              </div>
            </div>
            
            <div className="flex gap-2">
              <Button
                onClick={() => handleDownload('markdown')}
                disabled={downloading === 'markdown'}
                variant="outline"
                size="sm"
              >
                <Download className="w-4 h-4 mr-2" />
                {downloading === 'markdown' ? 'Downloading...' : 'Markdown'}
              </Button>
              <Button
                onClick={() => handleDownload('json')}
                disabled={downloading === 'json'}
                variant="outline"
                size="sm"
              >
                <Download className="w-4 h-4 mr-2" />
                {downloading === 'json' ? 'Downloading...' : 'JSON'}
              </Button>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        <Card className="mb-8 border-0 shadow-lg bg-gradient-to-r from-pink-50 to-purple-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-xl">
              <FileText className="w-5 h-5 text-pink-600" />
              Executive Summary
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 leading-relaxed">
              {briefing.synthesis_results.executive_summary}
            </p>
          </CardContent>
        </Card>

        {/* Key Insights */}
        {briefing.synthesis_results.key_insights.length > 0 && (
          <Card className="mb-8 border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <TrendingUp className="w-5 h-5 text-blue-600" />
                Key Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {briefing.synthesis_results.key_insights.map((insight, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{insight}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}

        {/* Trends Grid */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Trend Analysis</h2>
            <Badge variant="secondary" className="bg-pink-100 text-pink-800">
              {briefing.trend_analysis.trends.length} trends
            </Badge>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {briefing.trend_analysis.trends.map((trend, index) => (
              <TrendCard key={trend.id} trend={trend} index={index} />
            ))}
          </div>
        </div>

        {/* Actionable Recommendations */}
        {briefing.synthesis_results.actionable_recommendations.length > 0 && (
          <Card className="mb-8 border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <CheckCircle className="w-5 h-5 text-green-600" />
                Actionable Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {briefing.synthesis_results.actionable_recommendations.map((recommendation, index) => (
                  <div key={index} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                    <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{recommendation}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Market Outlook */}
        {briefing.synthesis_results.market_outlook && (
          <Card className="border-0 shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-xl">
                <BarChart3 className="w-5 h-5 text-purple-600" />
                Market Outlook
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 leading-relaxed">
                {briefing.synthesis_results.market_outlook}
              </p>
            </CardContent>
          </Card>
        )}
      </motion.div>
    </Navigation>
  );
} 