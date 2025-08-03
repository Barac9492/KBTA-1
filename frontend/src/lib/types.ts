export interface ScrapedPost {
  id: string;
  title: string;
  content: string;
  author: string;
  date: string;
  source: string;
  url: string;
}

export interface Trend {
  id: string;
  title: string;
  description: string;
  category: TrendCategory;
  business_impact: BusinessImpact;
  time_to_market: TimeToMarket;
  sources: string[];
  keywords: string[];
}

export interface PriorityTrend {
  id: string;
  title: string;
  description: string;
  reasoning: string;
  action_items: string[];
  business_impact: BusinessImpact;
}

export interface MarketOpportunity {
  id: string;
  title: string;
  description: string;
  market_size: string;
  entry_barriers: string[];
  competitive_advantage: string[];
}

export interface RiskFactor {
  id: string;
  title: string;
  description: string;
  severity: string;
  mitigation_strategies: string[];
}

export interface TrendAnalysis {
  trends: Trend[];
  priority_trends: PriorityTrend[];
  market_opportunities: MarketOpportunity[];
  risk_factors: RiskFactor[];
  summary: string;
}

export interface SynthesisResults {
  executive_summary: string;
  key_insights: string[];
  actionable_recommendations: string[];
  market_outlook: string;
}

export interface DailyBriefing {
  briefing_id: string;
  date: string;
  scraped_posts_count: number;
  trend_analysis: TrendAnalysis;
  synthesis_results: SynthesisResults;
}

export interface BriefingListItem {
  briefing_id: string;
  date: string;
  executive_summary: string;
  trends_count: number;
}

export enum TrendCategory {
  INGREDIENT = "ingredient",
  PRODUCT_TYPE = "product_type",
  CONSUMER_BEHAVIOR = "consumer_behavior",
  MARKET_TREND = "market_trend",
  TECHNOLOGY = "technology"
}

export enum BusinessImpact {
  HIGH = "high",
  MEDIUM = "medium",
  LOW = "low"
}

export enum TimeToMarket {
  IMMEDIATE = "immediate",
  SHORT_TERM = "short_term",
  MEDIUM_TERM = "medium_term",
  LONG_TERM = "long_term"
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface PipelineStatus {
  status: 'idle' | 'running' | 'completed' | 'failed';
  last_run?: string;
  next_run?: string;
  error?: string;
} 