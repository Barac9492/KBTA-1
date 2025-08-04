'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Trend, BusinessImpact, TrendCategory } from '@/lib/types';
import { 
  TrendingUp, 
  Clock, 
  Target, 
  Sparkles,
  Zap,
  ShoppingBag,
  Users,
  BarChart3,
  ExternalLink,
  Info,
  X
} from 'lucide-react';

interface TrendCardProps {
  trend: Trend;
  index: number;
}

const getImpactColor = (impact: BusinessImpact | string) => {
  switch (impact) {
    case BusinessImpact.HIGH:
    case 'high':
      return 'bg-red-100 text-red-800 border-red-200';
    case BusinessImpact.MEDIUM:
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case BusinessImpact.LOW:
    case 'low':
      return 'bg-green-100 text-green-800 border-green-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
};

const getCategoryIcon = (category: TrendCategory | string) => {
  switch (category) {
    case TrendCategory.INGREDIENT:
    case 'ingredient':
      return Sparkles;
    case TrendCategory.PRODUCT_TYPE:
    case 'product_type':
      return ShoppingBag;
    case TrendCategory.CONSUMER_BEHAVIOR:
    case 'consumer_behavior':
      return Users;
    case TrendCategory.MARKET_TREND:
    case 'market_trend':
      return TrendingUp;
    case TrendCategory.TECHNOLOGY:
    case 'technology':
      return Zap;
    default:
      return BarChart3;
  }
};

const getCategoryLabel = (category: TrendCategory | string) => {
  switch (category) {
    case TrendCategory.INGREDIENT:
    case 'ingredient':
      return '🧴 Ingredient';
    case TrendCategory.PRODUCT_TYPE:
    case 'product_type':
      return '🛍️ Product';
    case TrendCategory.CONSUMER_BEHAVIOR:
    case 'consumer_behavior':
      return '👥 Consumer';
    case TrendCategory.MARKET_TREND:
    case 'market_trend':
      return '📈 Market';
    case TrendCategory.TECHNOLOGY:
    case 'technology':
      return '⚡ Tech';
    default:
      return '📊 General';
  }
};

const getTimeToMarketColor = (timeToMarket: string) => {
  switch (timeToMarket) {
    case 'immediate':
      return 'bg-green-100 text-green-800';
    case 'short_term':
      return 'bg-blue-100 text-blue-800';
    case 'medium_term':
      return 'bg-yellow-100 text-yellow-800';
    case 'long_term':
      return 'bg-purple-100 text-purple-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export function TrendCard({ trend, index }: TrendCardProps) {
  const [showModal, setShowModal] = useState(false);
  const CategoryIcon = getCategoryIcon(trend.category);
  
  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: index * 0.1 }}
      >
        <Card 
          className="h-full border-0 glass-card trend-card-hover bg-white/90 backdrop-blur-sm cursor-pointer"
          onClick={() => setShowModal(true)}
        >
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <CategoryIcon className="w-5 h-5 text-pink-500" />
              <Badge variant="outline" className="text-xs">
                {getCategoryLabel(trend.category)}
              </Badge>
            </div>
            <Badge 
              variant="outline" 
              className={`text-xs font-medium ${getImpactColor(trend.business_impact)}`}
            >
              {trend.business_impact === BusinessImpact.HIGH || trend.business_impact === 'high' ? '🔥 High Impact' : 
               trend.business_impact === BusinessImpact.MEDIUM || trend.business_impact === 'medium' ? '⚡ Medium Impact' : '📈 Low Impact'}
            </Badge>
          </div>
          <CardTitle className="text-lg font-semibold text-gray-900 line-clamp-2">
            {trend.title}
          </CardTitle>
        </CardHeader>
        
        <CardContent className="pt-0">
          <p className="text-gray-600 text-sm leading-relaxed mb-4 line-clamp-3">
            {trend.description}
          </p>
          
          <div className="space-y-3">
            {/* Time to Market */}
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-gray-400" />
              <Badge 
                variant="outline" 
                className={`text-xs ${getTimeToMarketColor(trend.time_to_market || 'medium_term')}`}
              >
                {trend.time_to_market ? trend.time_to_market.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) : 'Medium Term'}
              </Badge>
            </div>
            
            {/* Keywords */}
            {trend.keywords && trend.keywords.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {trend.keywords.slice(0, 3).map((keyword, idx) => (
                  <Badge key={idx} variant="secondary" className="text-xs bg-pink-50 text-pink-700">
                    {keyword}
                  </Badge>
                ))}
                {trend.keywords.length > 3 && (
                  <Badge variant="secondary" className="text-xs bg-gray-50 text-gray-600">
                    +{trend.keywords.length - 3} more
                  </Badge>
                )}
              </div>
            )}
            
            {/* Sources */}
            {trend.sources && trend.sources.length > 0 && (
              <div className="flex items-center gap-2 text-xs text-gray-500">
                <Target className="w-3 h-3" />
                <span>{trend.sources.length} source{trend.sources.length !== 1 ? 's' : ''}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>

      {/* Trend Detail Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="glass-card rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto modal-enter"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <CategoryIcon className="w-6 h-6 text-pink-500" />
                  <Badge variant="outline" className="text-sm">
                    {getCategoryLabel(trend.category)}
                  </Badge>
                </div>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <h2 className="text-2xl font-bold text-gray-900 mb-4">{trend.title}</h2>
              
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700 leading-relaxed">{trend.description}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-2 flex items-center gap-2">
                      <Target className="w-4 h-4" />
                      Business Impact
                    </h3>
                    <Badge 
                      variant="outline" 
                      className={`text-sm font-medium ${getImpactColor(trend.business_impact)}`}
                    >
                      {trend.business_impact === BusinessImpact.HIGH || trend.business_impact === 'high' ? '🔥 High Impact' : 
                       trend.business_impact === BusinessImpact.MEDIUM || trend.business_impact === 'medium' ? '⚡ Medium Impact' : '📈 Low Impact'}
                    </Badge>
                  </div>

                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-2 flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      Time to Market
                    </h3>
                    <Badge 
                      variant="outline" 
                      className={`text-sm ${getTimeToMarketColor(trend.time_to_market || 'medium_term')}`}
                    >
                      {trend.time_to_market ? trend.time_to_market.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) : 'Medium Term'}
                    </Badge>
                  </div>
                </div>

                {trend.keywords && trend.keywords.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-2">Keywords</h3>
                    <div className="flex flex-wrap gap-2">
                      {trend.keywords.map((keyword, idx) => (
                        <Badge key={idx} variant="secondary" className="text-sm bg-pink-50 text-pink-700">
                          {keyword}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {trend.sources && trend.sources.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 mb-2 flex items-center gap-2">
                      <Info className="w-4 h-4" />
                      Sources ({trend.sources.length})
                    </h3>
                    <div className="space-y-2">
                      {trend.sources.map((source, idx) => (
                        <div key={idx} className="flex items-center gap-2 text-sm text-gray-600">
                          <ExternalLink className="w-4 h-4" />
                          <span className="capitalize">{source.replace('_', ' ')}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => setShowModal(false)}
                  className="w-full bg-pink-500 text-white px-4 py-2 rounded-md hover:bg-pink-600 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </>
  );
} 