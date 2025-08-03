'use client';

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
  Heart,
  Palette,
  ShoppingBag,
  Users,
  BarChart3
} from 'lucide-react';

interface TrendCardProps {
  trend: Trend;
  index: number;
}

const getImpactColor = (impact: BusinessImpact) => {
  switch (impact) {
    case BusinessImpact.HIGH:
      return 'bg-red-100 text-red-800 border-red-200';
    case BusinessImpact.MEDIUM:
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case BusinessImpact.LOW:
      return 'bg-green-100 text-green-800 border-green-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
};

const getCategoryIcon = (category: TrendCategory) => {
  switch (category) {
    case TrendCategory.INGREDIENT:
      return Sparkles;
    case TrendCategory.PRODUCT_TYPE:
      return ShoppingBag;
    case TrendCategory.CONSUMER_BEHAVIOR:
      return Users;
    case TrendCategory.MARKET_TREND:
      return TrendingUp;
    case TrendCategory.TECHNOLOGY:
      return Zap;
    default:
      return BarChart3;
  }
};

const getCategoryLabel = (category: TrendCategory) => {
  switch (category) {
    case TrendCategory.INGREDIENT:
      return '🧴 Ingredient';
    case TrendCategory.PRODUCT_TYPE:
      return '🛍️ Product';
    case TrendCategory.CONSUMER_BEHAVIOR:
      return '👥 Consumer';
    case TrendCategory.MARKET_TREND:
      return '📈 Market';
    case TrendCategory.TECHNOLOGY:
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
  const CategoryIcon = getCategoryIcon(trend.category);
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
    >
      <Card className="h-full border-0 shadow-lg hover:shadow-xl transition-shadow duration-300 bg-white">
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
              {trend.business_impact === BusinessImpact.HIGH ? '🔥 High Impact' : 
               trend.business_impact === BusinessImpact.MEDIUM ? '⚡ Medium Impact' : '📈 Low Impact'}
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
                className={`text-xs ${getTimeToMarketColor(trend.time_to_market)}`}
              >
                {trend.time_to_market.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
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
  );
} 