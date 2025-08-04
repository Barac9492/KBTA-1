'use client';

import { useState, useEffect } from 'react';
import { Navigation } from '@/components/Navigation';
import { TrendCard } from '@/components/TrendCard';
import { HeroSection } from '@/components/HeroSection';
import { apiClient } from '@/lib/api';
import { DailyBriefing } from '@/lib/types';

export default function Home() {
  const [briefing, setBriefing] = useState<DailyBriefing | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisStatus, setAnalysisStatus] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      console.log('useEffect triggered - starting data load');
      try {
        setLoading(true);
        setError(null);
        
        // Direct API call with timeout and retry logic
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout
        
        const response = await fetch('/api/latest', { 
          signal: controller.signal,
          headers: {
            'Content-Type': 'application/json',
          }
        });
        clearTimeout(timeoutId);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('API response:', data);
        
        if (data.status === 'success' && data.data) {
          console.log('Setting briefing data:', data.data);
          setBriefing(data.data);
        } else {
          console.log('API returned no data');
          setError('No briefing data available');
        }
      } catch (err) {
        console.error('Error loading briefing:', err);
        setError('Failed to load latest briefing');
      } finally {
        setLoading(false);
      }
    };
    
    console.log('Component mounted - calling loadData');
    // Add a small delay to ensure proper hydration
    setTimeout(() => {
      loadData();
    }, 100);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const loadLatestBriefing = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Loading latest briefing...');
      
      // Use direct fetch instead of apiClient to bypass any issues
      const response = await fetch('/api/latest');
      const data = await response.json();
      console.log('Direct API response:', data);
      
      if (data.status === 'success' && data.data) {
        console.log('Setting briefing data:', data.data);
        setBriefing(data.data);
        setLoading(false);
      } else {
        console.log('API call failed:', data);
        setError('Failed to load latest briefing');
        setLoading(false);
      }
    } catch (err) {
      console.error('Error loading briefing:', err);
      setError('Failed to load latest briefing');
      setLoading(false);
    }
  };

  const handleTriggerAnalysis = async () => {
    try {
      setAnalysisLoading(true);
      setAnalysisStatus('🚀 Starting analysis...');
      
      // Enhanced progress feedback with realistic timing
      const progressSteps = [
        { message: '📊 Scraping Korean beauty blogs and social media...', delay: 2000 },
        { message: '🤖 Processing data with AI models...', delay: 4000 },
        { message: '📈 Analyzing trends and patterns...', delay: 6000 },
        { message: '💡 Generating actionable insights...', delay: 8000 },
        { message: '📝 Creating executive summary...', delay: 10000 }
      ];

      // Start progress updates
      progressSteps.forEach((step, index) => {
        setTimeout(() => {
          if (analysisLoading) { // Only update if still loading
            setAnalysisStatus(step.message);
          }
        }, step.delay);
      });
      
      // Trigger the actual analysis
      const response = await apiClient.triggerBriefing();
      
      if (response.success) {
        setAnalysisStatus('✅ Analysis completed! Loading new data...');
        setTimeout(() => {
          loadLatestBriefing();
          setAnalysisStatus(null);
        }, 1500);
      } else {
        setAnalysisStatus('❌ Analysis failed. Please try again.');
        setTimeout(() => setAnalysisStatus(null), 3000);
      }
      
    } catch (err) {
      setAnalysisStatus('❌ Analysis failed. Please try again.');
      console.error('Error triggering analysis:', err);
      setTimeout(() => setAnalysisStatus(null), 3000);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const handleDownload = async (format: 'markdown' | 'json') => {
    try {
      if (format === 'markdown') {
        await downloadMarkdown();
      } else {
        await downloadJson();
      }
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  if (loading) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="relative mb-6">
              <div className="w-16 h-16 bg-kbeauty-gradient rounded-full flex items-center justify-center mx-auto">
                <svg className="w-8 h-8 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
              <div className="absolute inset-0 w-16 h-16 bg-pink-500/20 rounded-full animate-ping"></div>
            </div>
            <h2 className="text-xl font-semibold gradient-text mb-2">🌸 Loading K-Beauty Insights</h2>
            <p className="text-gray-600 mb-4">Analyzing the latest trends from Korean beauty sources...</p>
            <div className="w-48 h-2 bg-pink-100 rounded-full mx-auto overflow-hidden">
              <div className="progress-glow h-2 rounded-full" style={{ width: '60%' }}></div>
            </div>
            {/* Fallback content that shows after 10 seconds */}
            <div className="mt-8 text-sm text-gray-500">
              <p>If this takes too long, try refreshing the page</p>
              <button 
                onClick={() => window.location.reload()} 
                className="mt-2 text-pink-500 hover:text-pink-600 underline"
              >
                Refresh Page
              </button>
            </div>
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
            <div className="text-red-500 mb-4">
              <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">Failed to load briefing</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <div className="space-x-2">
              <button
                onClick={() => {
                  setError(null);
                  setLoading(true);
                  loadLatestBriefing();
                }}
                className="bg-pink-500 text-white px-4 py-2 rounded-md hover:bg-pink-600 transition-colors"
              >
                Try Again
              </button>
              <button
                onClick={() => window.location.reload()}
                className="bg-gray-500 text-white px-4 py-2 rounded-md hover:bg-gray-600 transition-colors"
              >
                Refresh Page
              </button>
              <button
                onClick={handleTriggerAnalysis}
                className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600 transition-colors"
              >
                Run New Analysis
              </button>
            </div>
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
            <div className="text-gray-400 mb-4">
              <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No briefing available</h3>
            <p className="text-gray-600 mb-4">Start your first analysis to see K-beauty trends</p>
            <button
              onClick={handleTriggerAnalysis}
              disabled={analysisLoading}
              className="bg-pink-500 text-white px-4 py-2 rounded-md hover:bg-pink-600 transition-colors disabled:opacity-50"
            >
              {analysisLoading ? 'Starting Analysis...' : 'Start Analysis'}
            </button>
          </div>
        </div>
      </Navigation>
    );
  }

  return (
    <Navigation>
      {/* Enhanced Hero Section */}
      <div className="mb-8">
        <HeroSection 
          briefingCount={briefing.scraped_posts_count} 
          lastUpdated={formatDate(briefing.date)}
        />
        
        {/* Action Buttons */}
        <div className="flex justify-end space-x-3 mt-4">
          <button
            onClick={() => handleDownload('markdown')}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-all duration-300 text-sm font-medium"
          >
            📄 Download MD
          </button>
          <button
            onClick={() => handleDownload('json')}
            className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-all duration-300 text-sm font-medium"
          >
            📊 Download JSON
          </button>
          <button
            onClick={handleTriggerAnalysis}
            disabled={analysisLoading}
            className="btn-kbeauty text-white px-6 py-3 rounded-lg font-medium disabled:opacity-50 text-sm relative overflow-hidden"
          >
            <span className="relative z-10">{analysisLoading ? '🔄 Running...' : '✨ New Analysis'}</span>
          </button>
        </div>
          
        {/* Analysis Status */}
        {analysisLoading && analysisStatus && (
          <div className="mb-4 p-4 glass-card border border-pink-200 rounded-lg">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <div className="relative">
                  <svg className="w-6 h-6 text-pink-500 animate-spin mr-3" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <div className="absolute inset-0 w-6 h-6 bg-pink-500/20 rounded-full animate-ping"></div>
                </div>
                <span className="text-pink-700 font-medium text-lg">{analysisStatus}</span>
              </div>
              <span className="text-xs text-pink-600 bg-pink-100 px-3 py-1 rounded-full font-medium">
                🤖 AI Processing
              </span>
            </div>
            <div className="w-full bg-pink-100 rounded-full h-3 overflow-hidden">
              <div className="progress-glow h-3 rounded-full" style={{ width: '75%' }}></div>
            </div>
          </div>
        )}

        <div className="prose max-w-none">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Executive Summary</h2>
          <p className="text-gray-700 mb-4">{briefing.synthesis_results.executive_summary}</p>
          
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Key Insights</h2>
          <ul className="list-disc list-inside text-gray-700 mb-4 space-y-1">
            {briefing.synthesis_results.key_insights.map((insight, index) => (
              <li key={index}>{insight}</li>
            ))}
          </ul>
          
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Actionable Recommendations</h2>
          <ul className="list-disc list-inside text-gray-700 mb-4 space-y-1">
            {briefing.synthesis_results.actionable_recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
          
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Market Outlook</h2>
          <p className="text-gray-700">{briefing.synthesis_results.market_outlook}</p>
        </div>
      </div>

      {/* Trends Grid */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Trend Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {briefing.trend_analysis.trends.map((trend) => (
            <TrendCard key={trend.id} trend={trend} index={0} />
          ))}
        </div>
      </div>
    </Navigation>
  );
}

function formatDate(dateString: string): string {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch {
    return 'Unknown date';
  }
}

async function downloadMarkdown() {
  // Implementation for markdown download
  console.log('Downloading markdown...');
}

async function downloadJson() {
  // Implementation for JSON download
  console.log('Downloading JSON...');
}
