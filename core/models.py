"""
Data models for K-Beauty Trend Briefing System
"""

import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class TrendCategory(Enum):
    """Categories for K-beauty trends."""
    SKINCARE = "skincare"
    MAKEUP = "makeup"
    HAIR = "hair"
    FRAGRANCE = "fragrance"
    TOOLS = "tools"
    INGREDIENTS = "ingredients"
    PACKAGING = "packaging"
    SUSTAINABILITY = "sustainability"
    TECHNOLOGY = "technology"
    GENERAL = "general"

class BusinessImpact(Enum):
    """Business impact levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TrendType(Enum):
    """Types of trends."""
    EMERGING = "emerging"
    GROWING = "growing"
    PEAK = "peak"
    DECLINING = "declining"

class TimeToMarket(Enum):
    """Time to market for trends."""
    IMMEDIATE = "immediate"
    SHORT_TERM = "short_term"
    MEDIUM_TERM = "medium_term"
    LONG_TERM = "long_term"

@dataclass
class ScrapedPost:
    """Represents a scraped post from social media."""
    title: str
    content: str
    source: str
    url: Optional[str] = None
    date: Optional[datetime] = None
    author: Optional[str] = None
    engagement: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        if self.date:
            data['date'] = self.date.isoformat()
        return data

@dataclass
class Trend:
    """Represents a K-beauty trend."""
    trend_name: str
    description: str
    confidence: float
    category: TrendCategory
    business_impact: BusinessImpact
    sources: List[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.sources is None:
            self.sources = []
        if self.keywords is None:
            self.keywords = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'trend_name': self.trend_name,
            'description': self.description,
            'confidence': self.confidence,
            'category': self.category.value,
            'business_impact': self.business_impact.value,
            'sources': self.sources,
            'keywords': self.keywords
        }

@dataclass
class TrendAnalysis:
    """Represents the analysis of trends from scraped content."""
    trends: List[Trend]
    analysis_date: datetime
    total_posts_analyzed: int
    confidence_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'trends': [trend.to_dict() for trend in self.trends],
            'analysis_date': self.analysis_date.isoformat(),
            'total_posts_analyzed': self.total_posts_analyzed,
            'confidence_score': self.confidence_score
        }

@dataclass
class PriorityTrend:
    """Represents a priority trend for business action."""
    rank: int
    trend_name: str
    reasoning: str
    business_impact: BusinessImpact
    action_items: List[str] = None
    
    def __post_init__(self):
        if self.action_items is None:
            self.action_items = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'rank': self.rank,
            'trend_name': self.trend_name,
            'reasoning': self.reasoning,
            'business_impact': self.business_impact.value,
            'action_items': self.action_items
        }

@dataclass
class MarketOpportunity:
    """Represents a market opportunity."""
    opportunity_name: str
    description: str
    potential_value: str
    time_horizon: str
    action_items: List[str] = None
    
    def __post_init__(self):
        if self.action_items is None:
            self.action_items = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'opportunity_name': self.opportunity_name,
            'description': self.description,
            'potential_value': self.potential_value,
            'time_horizon': self.time_horizon,
            'action_items': self.action_items
        }

@dataclass
class RiskFactor:
    """Represents a risk factor."""
    risk_name: str
    description: str
    severity: str
    mitigation_strategies: List[str] = None
    
    def __post_init__(self):
        if self.mitigation_strategies is None:
            self.mitigation_strategies = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'risk_name': self.risk_name,
            'description': self.description,
            'severity': self.severity,
            'mitigation_strategies': self.mitigation_strategies
        }

@dataclass
class SynthesisResults:
    """Represents the synthesis of trend analysis into actionable insights."""
    priority_trends: List[PriorityTrend]
    market_opportunities: List[MarketOpportunity]
    risk_factors: List[RiskFactor]
    executive_summary: str
    synthesis_date: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'priority_trends': [trend.to_dict() for trend in self.priority_trends],
            'market_opportunities': [opp.to_dict() for opp in self.market_opportunities],
            'risk_factors': [risk.to_dict() for risk in self.risk_factors],
            'executive_summary': self.executive_summary,
            'synthesis_date': self.synthesis_date.isoformat()
        }

@dataclass
class DailyBriefing:
    """Represents a complete daily briefing."""
    briefing_id: str
    date: datetime
    scraped_posts_count: int
    trend_analysis: TrendAnalysis
    synthesis_results: SynthesisResults
    
    def __post_init__(self):
        if not self.briefing_id:
            self.briefing_id = f"briefing_{self.date.strftime('%Y%m%d_%H%M%S')}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'briefing_id': self.briefing_id,
            'date': self.date.isoformat(),
            'scraped_posts_count': self.scraped_posts_count,
            'trend_analysis': self.trend_analysis.to_dict(),
            'synthesis_results': self.synthesis_results.to_dict()
        }
    
    def to_markdown(self) -> str:
        """Convert to markdown format."""
        md = f"""# K-Beauty Daily Trend Briefing
**Date:** {self.date.strftime('%Y-%m-%d %H:%M:%S')}
**Briefing ID:** {self.briefing_id}
**Posts Analyzed:** {self.scraped_posts_count}

## Executive Summary
{self.synthesis_results.executive_summary}

## Priority Trends
"""
        
        for trend in self.synthesis_results.priority_trends:
            md += f"""
### {trend.rank}. {trend.trend_name}
**Business Impact:** {trend.business_impact.value.title()}
**Reasoning:** {trend.reasoning}

**Action Items:**
"""
            for item in trend.action_items:
                md += f"- {item}\n"
        
        md += "\n## Market Opportunities\n"
        for opp in self.synthesis_results.market_opportunities:
            md += f"""
### {opp.opportunity_name}
**Description:** {opp.description}
**Potential Value:** {opp.potential_value}
**Time Horizon:** {opp.time_horizon}

**Action Items:**
"""
            for item in opp.action_items:
                md += f"- {item}\n"
        
        md += "\n## Risk Factors\n"
        for risk in self.synthesis_results.risk_factors:
            md += f"""
### {risk.risk_name}
**Severity:** {risk.severity.title()}
**Description:** {risk.description}

**Mitigation Strategies:**
"""
            for strategy in risk.mitigation_strategies:
                md += f"- {strategy}\n"
        
        md += f"""
## Trend Analysis
**Total Trends Identified:** {len(self.trend_analysis.trends)}
**Confidence Score:** {self.trend_analysis.confidence_score:.2f}

### Identified Trends
"""
        
        for trend in self.trend_analysis.trends:
            md += f"""
#### {trend.trend_name}
**Category:** {trend.category.value.title()}
**Confidence:** {trend.confidence:.2f}
**Business Impact:** {trend.business_impact.value.title()}
**Description:** {trend.description}

**Keywords:** {', '.join(trend.keywords)}
"""
        
        return md

class PipelineStatus(Enum):
    """Pipeline status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class PipelineStatus:
    """Represents the status of the daily briefing pipeline."""
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    briefing_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'status': self.status,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'error_message': self.error_message,
            'briefing_id': self.briefing_id
        }

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj) 