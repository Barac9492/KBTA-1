'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Navigation } from '@/components/Navigation';
import { apiClient } from '@/lib/api';
import { BriefingListItem } from '@/lib/types';
import { 
  Search, 
  Filter, 
  Calendar,
  TrendingUp,
  FileText,
  Download,
  RefreshCw,
  AlertCircle
} from 'lucide-react';

export default function ArchivePage() {
  const [briefings, setBriefings] = useState<BriefingListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState<string>('all');

  useEffect(() => {
    loadBriefings();
  }, []);

  const loadBriefings = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Loading briefings...');
      const response = await apiClient.getBriefings();
      console.log('API response:', response);
      if (response.success && response.data) {
        console.log('Setting briefings data:', response.data);
        setBriefings(response.data);
      } else {
        console.log('API call failed:', response.error);
        setError(response.error || 'Failed to load briefings');
      }
    } catch {
      console.log('Exception caught');
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return 'No date available';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Invalid date';
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (error) {
      return 'Invalid date';
    }
  };

  const filteredBriefings = (briefings || []).filter(briefing => {
    const matchesSearch = briefing.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         briefing.briefing_id?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterCategory === 'all' || briefing.category === filterCategory;
    return matchesSearch && matchesFilter;
  });

  console.log('Briefings state:', briefings);
  console.log('Filtered briefings:', filteredBriefings);

  if (loading) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <RefreshCw className="w-8 h-8 text-pink-500 animate-spin mx-auto mb-4" />
            <p className="text-gray-600">Loading archive...</p>
          </div>
        </div>
      </Navigation>
    );
  }

  if (error) {
    return (
      <Navigation>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center max-w-md">
            <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Error Loading Archive</h3>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Briefing Archive</h1>
          <p className="text-gray-600">Browse and search through past K-beauty trend briefings</p>
        </div>

        {/* Search and Filter */}
        <Card className="mb-8 border-0 shadow-lg">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search briefings..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                />
              </div>
              
              {/* Filter */}
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <select
                  value={filterCategory}
                  onChange={(e) => setFilterCategory(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                >
                  <option value="all">All Categories</option>
                  <option value="SKIN_CARE">Skin Care</option>
                  <option value="MAKEUP">Makeup</option>
                  <option value="INGREDIENTS">Ingredients</option>
                  <option value="PACKAGING">Packaging</option>
                </select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              {filteredBriefings.length} Briefing{filteredBriefings.length !== 1 ? 's' : ''}
            </h2>
            <Badge variant="secondary" className="bg-pink-100 text-pink-800">
              {briefings.length} total
            </Badge>
          </div>

          {filteredBriefings.length === 0 ? (
            <Card className="border-0 shadow-lg">
              <CardContent className="p-8 text-center">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">No Briefings Found</h3>
                <p className="text-gray-600 mb-4">
                  {searchTerm || filterCategory !== 'all' 
                    ? 'Try adjusting your search or filter criteria.'
                    : 'No briefings have been generated yet. Run your first analysis to get started.'
                  }
                </p>
                {!searchTerm && filterCategory === 'all' && (
                  <Button className="bg-pink-500 hover:bg-pink-600">
                    <TrendingUp className="w-4 h-4 mr-2" />
                    Run First Analysis
                  </Button>
                )}
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-6">
              {filteredBriefings.map((briefing, index) => (
                <motion.div
                  key={briefing.briefing_id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <Card className="border-0 shadow-lg hover:shadow-xl transition-shadow">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div>
                          <CardTitle className="text-lg mb-2">{briefing.title || `Briefing ${briefing.briefing_id}`}</CardTitle>
                          <div className="flex items-center gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-2">
                              <Calendar className="w-4 h-4" />
                              {formatDate(briefing.date)}
                            </div>
                            <div className="flex items-center gap-2">
                              <TrendingUp className="w-4 h-4" />
                              {briefing.trend_count || 0} trends
                            </div>
                            <div className="flex items-center gap-2">
                              <FileText className="w-4 h-4" />
                              {briefing.source_count || 0} sources
                            </div>
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button variant="outline" size="sm">
                            <Download className="w-4 h-4 mr-2" />
                            JSON
                          </Button>
                          <Button variant="outline" size="sm">
                            <Download className="w-4 h-4 mr-2" />
                            Markdown
                          </Button>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-600 mb-4 line-clamp-3">
                        {briefing.summary || 'No summary available for this briefing.'}
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {briefing.categories?.map((category: string, idx: number) => (
                          <Badge key={idx} variant="secondary" className="text-xs">
                            {category}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </motion.div>
    </Navigation>
  );
} 