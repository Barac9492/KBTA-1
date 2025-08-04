'use client';

import { motion } from 'framer-motion';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { BriefingListItem as BriefingItem } from '@/lib/types';
import { Calendar, FileText, TrendingUp, Eye } from 'lucide-react';

interface BriefingListItemProps {
  briefing: BriefingItem;
  onView: (id: string) => void;
  index: number;
}

export function BriefingListItem({ briefing, onView, index }: BriefingListItemProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const truncateSummary = (summary: string, maxLength: number = 150) => {
    if (summary.length <= maxLength) return summary;
    return summary.substring(0, maxLength) + '...';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ scale: 1.01 }}
    >
      <Card className="border-0 shadow-md hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-pink-50 to-purple-50">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-pink-100 rounded-lg">
                <Calendar className="w-5 h-5 text-pink-600" />
              </div>
              <div>
                <CardTitle className="text-lg font-semibold text-gray-800">
                  {formatDate(briefing.date)}
                </CardTitle>
                <p className="text-sm text-gray-500">
                  Briefing #{briefing.briefing_id}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                <TrendingUp className="w-3 h-3 mr-1" />
                {briefing.trends_count} trends
              </Badge>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="pt-0">
          <p className="text-gray-600 text-sm leading-relaxed mb-4">
            {truncateSummary(briefing.executive_summary)}
          </p>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <FileText className="w-4 h-4" />
              <span>Executive summary available</span>
            </div>
            
            <Button 
              onClick={() => onView(briefing.briefing_id)}
              size="sm"
              className="bg-pink-500 hover:bg-pink-600 text-white"
            >
              <Eye className="w-4 h-4 mr-2" />
              View Details
            </Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
} 