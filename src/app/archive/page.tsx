'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Navigation } from '@/components/Navigation';
import { BriefingListItem } from '@/components/BriefingListItem';
import { apiClient } from '@/lib/api';
import { BriefingListItem as BriefingItem, DailyBriefing } from '@/lib/types';
import { 
  Search, 
  Archive, 
  RefreshCw, 
  AlertCircle,
  Filter,
  Calendar,
  TrendingUp
} from 'lucide-react';

export default function ArchivePage() {
  const [briefings, setBriefings] = useState<BriefingItem[]>([]);
  const [filteredBriefings, setFilteredBriefings] = useState<BriefingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBriefing, setSelectedBriefing] = useState<DailyBriefing | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    loadBriefings();
  }, []);

  useEffect(() => {
    filterBriefings();
  }, [searchTerm, briefings]);

  const loadBriefings = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getBriefings();
      if (response.success && response.data) {
        setBriefings(response.data);
      } else {
        setError(response.error || 'Failed to load briefings');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const filterBriefings = () => {
    if (!searchTerm.trim()) {
      setFilteredBriefings(briefings);
      return;
    }

    const filtered = briefings.filter(briefing => 
      briefing.executive_summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
      briefing.briefing_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      briefing.date.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredBriefings(filtered);
  };

  const handleViewBriefing = async (id: string) => {
    try {
      const response = await apiClient.getBriefing(id);
      if (response.success && response.data) {
        setSelectedBriefing(response.data);
        setShowModal(true);
      } else {
        setError('Failed to load briefing details');
      }
    } catch (err) {
      setError('Failed to load briefing details');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 text-pink-500 animate-spin mx-auto mb-4" />
            <p className="text-gray-600">Loading briefings...</p>
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
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Briefings</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={loadBriefings} className="bg-pink-500 hover:bg-pink-600">
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again
            </Button>
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
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Briefing Archive
              </h1>
              <p className="text-gray-600">
                Browse all past K-beauty trend briefings
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Archive className="w-6 h-6 text-pink-500" />
              <Badge variant="secondary" className="bg-pink-100 text-pink-800">
                {briefings.length} briefings
              </Badge>
            </div>
          </div>

          {/* Search and Filter */}
          <div className="flex items-center gap-4 mb-6">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search briefings..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
              />
            </div>
            <Button
              onClick={loadBriefings}
              variant="outline"
              size="sm"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
          </div>
        </div>

        {/* Results */}
        {filteredBriefings.length === 0 ? (
          <Card className="border-0 shadow-lg">
            <CardContent className="py-12">
              <div className="text-center">
                <Archive className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {searchTerm ? 'No matching briefings' : 'No briefings available'}
                </h3>
                <p className="text-gray-600">
                  {searchTerm 
                    ? 'Try adjusting your search terms'
                    : 'No briefings have been generated yet.'
                  }
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredBriefings.map((briefing, index) => (
              <BriefingListItem
                key={briefing.briefing_id}
                briefing={briefing}
                onView={handleViewBriefing}
                index={index}
              />
            ))}
          </div>
        )}

        {/* Briefing Detail Modal */}
        {showModal && selectedBriefing && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <div className="fixed inset-0 bg-black bg-opacity-50" onClick={() => setShowModal(false)} />
            <div className="relative bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">
                      Briefing Details
                    </h2>
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4" />
                        {formatDate(selectedBriefing.date)}
                      </div>
                      <div className="flex items-center gap-2">
                        <TrendingUp className="w-4 h-4" />
                        {selectedBriefing.trend_analysis.trends.length} trends
                      </div>
                    </div>
                  </div>
                  <Button
                    onClick={() => setShowModal(false)}
                    variant="ghost"
                    size="sm"
                  >
                    ×
                  </Button>
                </div>

                {/* Executive Summary */}
                <Card className="mb-6 border-0 shadow-md">
                  <CardHeader>
                    <CardTitle className="text-lg">Executive Summary</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-700 leading-relaxed">
                      {selectedBriefing.synthesis_results.executive_summary}
                    </p>
                  </CardContent>
                </Card>

                {/* Key Insights */}
                {selectedBriefing.synthesis_results.key_insights.length > 0 && (
                  <Card className="mb-6 border-0 shadow-md">
                    <CardHeader>
                      <CardTitle className="text-lg">Key Insights</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {selectedBriefing.synthesis_results.key_insights.map((insight, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                            <span className="text-gray-700">{insight}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                )}

                {/* Trends */}
                <Card className="mb-6 border-0 shadow-md">
                  <CardHeader>
                    <CardTitle className="text-lg">Trend Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {selectedBriefing.trend_analysis.trends.map((trend, index) => (
                        <div key={trend.id} className="p-4 bg-gray-50 rounded-lg">
                          <h4 className="font-semibold text-gray-900 mb-2">{trend.title}</h4>
                          <p className="text-sm text-gray-600 mb-3">{trend.description}</p>
                          <div className="flex gap-2">
                            <Badge variant="outline" className="text-xs">
                              {trend.business_impact} impact
                            </Badge>
                            <Badge variant="outline" className="text-xs">
                              {trend.time_to_market}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Actionable Recommendations */}
                {selectedBriefing.synthesis_results.actionable_recommendations.length > 0 && (
                  <Card className="border-0 shadow-md">
                    <CardHeader>
                      <CardTitle className="text-lg">Actionable Recommendations</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {selectedBriefing.synthesis_results.actionable_recommendations.map((recommendation, index) => (
                          <div key={index} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                            <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0" />
                            <span className="text-gray-700">{recommendation}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </Navigation>
  );
} 