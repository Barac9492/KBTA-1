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
      return <Sparkles className="w-4 h-4" />;
    case TrendCategory.PRODUCT_TYPE:
      return <ShoppingBag className="w-4 h-4" />;
    case TrendCategory.CONSUMER_BEHAVIOR:
      return <Users className="w-4 h-4" />;
    case TrendCategory.MARKET_TREND:
      return <BarChart3 className="w-4 h-4" />;
    case TrendCategory.TECHNOLOGY:
      return <Zap className="w-4 h-4" />;
    default:
      return <TrendingUp className="w-4 h-4" />;
  }
};

const getCategoryLabel = (category: TrendCategory) => {
  switch (category) {
    case TrendCategory.INGREDIENT:
      return '🧴 Ingredient';
    case TrendCategory.PRODUCT_TYPE:
      return '💄 Product';
    case TrendCategory.CONSUMER_BEHAVIOR:
      return '👥 Consumer';
    case TrendCategory.MARKET_TREND:
      return '📈 Market';
    case TrendCategory.TECHNOLOGY:
      return '⚡ Tech';
    default:
      return '📊 Trend';
  }
};

const getTimeToMarketColor = (timeToMarket: string) => {
  switch (timeToMarket) {
    case 'immediate':
      return 'bg-emerald-100 text-emerald-800 border-emerald-200';
    case 'short_term':
      return 'bg-blue-100 text-blue-800 border-blue-200';
    case 'medium_term':
      return 'bg-orange-100 text-orange-800 border-orange-200';
    case 'long_term':
      return 'bg-purple-100 text-purple-800 border-purple-200';
    default:
      return 'bg-gray-100 text-gray-800 border-gray-200';
  }
};

export function TrendCard({ trend, index }: TrendCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ scale: 1.02 }}
      className="h-full"
    >
      <Card className="h-full border-0 shadow-lg bg-gradient-to-br from-pink-50 to-purple-50 hover:shadow-xl transition-all duration-300">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              {getCategoryIcon(trend.category)}
              <CardTitle className="text-lg font-semibold text-gray-800">
                {trend.title}
              </CardTitle>
            </div>
            <div className="flex flex-col gap-1">
              <Badge 
                variant="outline" 
                className={`text-xs font-medium ${getImpactColor(trend.business_impact)}`}
              >
                {trend.business_impact === BusinessImpact.HIGH ? '🔥 High Impact' : 
                 trend.business_impact === BusinessImpact.MEDIUM ? '⚡ Medium Impact' : 
                 '💡 Low Impact'}
              </Badge>
              <Badge 
                variant="outline" 
                className={`text-xs font-medium ${getTimeToMarketColor(trend.time_to_market)}`}
              >
                <Clock className="w-3 h-3 mr-1" />
                {trend.time_to_market.replace('_', ' ')}
              </Badge>
            </div>
          </div>
          <Badge variant="secondary" className="w-fit text-xs">
            {getCategoryLabel(trend.category)}
          </Badge>
        </CardHeader>
        
        <CardContent className="pt-0">
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            {trend.description}
          </p>
          
          {trend.keywords.length > 0 && (
            <div className="mb-3">
              <p className="text-xs font-medium text-gray-500 mb-2">Keywords:</p>
              <div className="flex flex-wrap gap-1">
                {trend.keywords.slice(0, 5).map((keyword, idx) => (
                  <Badge 
                    key={idx} 
                    variant="outline" 
                    className="text-xs bg-white/50 border-gray-200"
                  >
                    {keyword}
                  </Badge>
                ))}
                {trend.keywords.length > 5 && (
                  <Badge variant="outline" className="text-xs bg-white/50 border-gray-200">
                    +{trend.keywords.length - 5} more
                  </Badge>
                )}
              </div>
            </div>
          )}
          
          {trend.sources.length > 0 && (
            <div className="text-xs text-gray-500">
              <span className="font-medium">Sources:</span> {trend.sources.length} found
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
} 