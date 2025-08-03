"""
AI Agents for K-Beauty Trend Analysis
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

import openai
from core.config import config
from core.models import (
    ScrapedPost, TrendAnalysis, Trend, 
    SynthesisResults, PriorityTrend, MarketOpportunity, RiskFactor,
    BusinessImpact, TrendCategory
)

logger = logging.getLogger(__name__)

class TrendResearcherAgent:
    """AI agent for analyzing K-beauty trends from scraped content."""
    
    def __init__(self):
        self.model = config.llm.model
        self.max_tokens = config.llm.max_tokens
        self.temperature = config.llm.temperature
        
        # Load the trend researcher prompt
        prompt_path = Path("agents/trend-researcher.md")
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.prompt_template = f.read()
        else:
            logger.warning("trend-researcher.md not found, using default prompt")
            self.prompt_template = self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default prompt if markdown file is not found."""
        return """
You are a K-beauty trend researcher analyzing social media content to identify emerging trends.

Analyze the provided content and identify trends with the following criteria:
- Relevance to K-beauty market
- Growth potential
- Consumer interest
- Innovation level

Output format: JSON with trends array containing trend_name, description, confidence, category, and business_impact.
"""
    
    async def analyze_trends(self, posts: List[ScrapedPost]) -> TrendAnalysis:
        """Analyze scraped posts to identify K-beauty trends."""
        logger.info(f"Analyzing {len(posts)} posts for trends...")
        
        # Prepare content for analysis
        content_summary = self._prepare_content_summary(posts)
        
        # Create the prompt
        prompt = self.prompt_template + f"\n\nContent to analyze:\n{content_summary}"
        
        try:
            # Call OpenAI API (v0.28.1 async)
            response = await openai.ChatCompletion.acreate(
                api_key=config.llm.openai_api_key,
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a K-beauty trend researcher. Analyze the content and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response
            content = response["choices"][0]["message"]["content"]
            trends_data = self._parse_json_response(content)
            
            # Convert to Trend objects
            trends = []
            for trend_data in trends_data.get('trends', []):
                trend = Trend(
                    trend_name=trend_data.get('trend_name', ''),
                    description=trend_data.get('description', ''),
                    confidence=trend_data.get('confidence', 0.0),
                    category=TrendCategory(trend_data.get('category', 'general')),
                    business_impact=BusinessImpact(trend_data.get('business_impact', 'low')),
                    sources=trend_data.get('sources', []),
                    keywords=trend_data.get('keywords', [])
                )
                trends.append(trend)
            
            return TrendAnalysis(
                trends=trends,
                analysis_date=datetime.now(),
                total_posts_analyzed=len(posts),
                confidence_score=trends_data.get('confidence_score', 0.0)
            )
            
        except Exception as e:
            logger.error(f"Error in trend analysis: {e}")
            # Return empty analysis on error
            return TrendAnalysis(
                trends=[],
                analysis_date=datetime.now(),
                total_posts_analyzed=len(posts),
                confidence_score=0.0
            )
    
    def _prepare_content_summary(self, posts: List[ScrapedPost]) -> str:
        """Prepare content summary for analysis."""
        summary_parts = []
        
        for i, post in enumerate(posts[:20]):  # Limit to first 20 posts
            summary_parts.append(f"Post {i+1}:")
            summary_parts.append(f"Title: {post.title}")
            summary_parts.append(f"Content: {post.content[:200]}...")
            summary_parts.append(f"Source: {post.source}")
            summary_parts.append(f"Date: {post.date}")
            summary_parts.append("---")
        
        return "\n".join(summary_parts)
    
    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON response from AI model."""
        try:
            # Try to extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                logger.error("No JSON found in response")
                return {"trends": []}
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {"trends": []}

class FeedbackSynthesizerAgent:
    """AI agent for synthesizing feedback and creating actionable insights."""
    
    def __init__(self):
        self.model = config.llm.model
        self.max_tokens = config.llm.max_tokens
        self.temperature = config.llm.temperature
        
        # Load the feedback synthesizer prompt
        prompt_path = Path("agents/feedback-synthesizer.md")
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                self.prompt_template = f.read()
        else:
            logger.warning("feedback-synthesizer.md not found, using default prompt")
            self.prompt_template = self._get_default_prompt()
    
    def _get_default_prompt(self) -> str:
        """Default prompt if markdown file is not found."""
        return """
You are a K-beauty market analyst synthesizing trend data into actionable insights.

Analyze the trends and provide:
- Priority trends for immediate action
- Market opportunities
- Risk factors
- Executive summary

Output format: JSON with synthesis results.
"""
    
    async def synthesize_feedback(self, trend_analysis: TrendAnalysis) -> SynthesisResults:
        """Synthesize trend analysis into actionable insights."""
        logger.info("Synthesizing trend analysis into actionable insights...")
        
        # Prepare trend data for synthesis
        trends_summary = self._prepare_trends_summary(trend_analysis)
        
        # Create the prompt
        prompt = self.prompt_template + f"\n\nTrend Analysis:\n{trends_summary}"
        
        try:
            # Call OpenAI API (v0.28.1 async)
            response = await openai.ChatCompletion.acreate(
                api_key=config.llm.openai_api_key,
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a K-beauty market analyst. Analyze the trends and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response
            content = response["choices"][0]["message"]["content"]
            synthesis_data = self._parse_json_response(content)
            
            # Convert to SynthesisResults object
            return SynthesisResults(
                priority_trends=self._parse_priority_trends(synthesis_data.get('priority_trends', [])),
                market_opportunities=self._parse_market_opportunities(synthesis_data.get('market_opportunities', [])),
                risk_factors=self._parse_risk_factors(synthesis_data.get('risk_factors', [])),
                executive_summary=synthesis_data.get('executive_summary', ''),
                synthesis_date=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error in feedback synthesis: {e}")
            # Return empty synthesis on error
            return SynthesisResults(
                priority_trends=[],
                market_opportunities=[],
                risk_factors=[],
                executive_summary="Analysis failed",
                synthesis_date=datetime.now()
            )
    
    def _prepare_trends_summary(self, trend_analysis: TrendAnalysis) -> str:
        """Prepare trends summary for synthesis."""
        summary_parts = []
        
        for trend in trend_analysis.trends:
            summary_parts.append(f"Trend: {trend.trend_name}")
            summary_parts.append(f"Description: {trend.description}")
            summary_parts.append(f"Confidence: {trend.confidence}")
            summary_parts.append(f"Category: {trend.category.value}")
            summary_parts.append(f"Business Impact: {trend.business_impact.value}")
            summary_parts.append("---")
        
        return "\n".join(summary_parts)
    
    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON response from AI model."""
        try:
            # Try to extract JSON from the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            else:
                logger.error("No JSON found in response")
                return {}
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {}
    
    def _parse_priority_trends(self, trends_data: List[Dict]) -> List[PriorityTrend]:
        """Parse priority trends from synthesis data."""
        priority_trends = []
        for i, trend_data in enumerate(trends_data):
            priority_trend = PriorityTrend(
                rank=i + 1,
                trend_name=trend_data.get('trend_name', ''),
                reasoning=trend_data.get('reasoning', ''),
                business_impact=BusinessImpact(trend_data.get('business_impact', 'low')),
                action_items=trend_data.get('action_items', [])
            )
            priority_trends.append(priority_trend)
        return priority_trends
    
    def _parse_market_opportunities(self, opportunities_data: List[Dict]) -> List[MarketOpportunity]:
        """Parse market opportunities from synthesis data."""
        opportunities = []
        for opportunity_data in opportunities_data:
            opportunity = MarketOpportunity(
                opportunity_name=opportunity_data.get('opportunity_name', ''),
                description=opportunity_data.get('description', ''),
                potential_value=opportunity_data.get('potential_value', ''),
                time_horizon=opportunity_data.get('time_horizon', ''),
                action_items=opportunity_data.get('action_items', [])
            )
            opportunities.append(opportunity)
        return opportunities
    
    def _parse_risk_factors(self, risks_data: List[Dict]) -> List[RiskFactor]:
        """Parse risk factors from synthesis data."""
        risk_factors = []
        for risk_data in risks_data:
            risk_factor = RiskFactor(
                risk_name=risk_data.get('risk_name', ''),
                description=risk_data.get('description', ''),
                severity=risk_data.get('severity', 'low'),
                mitigation_strategies=risk_data.get('mitigation_strategies', [])
            )
            risk_factors.append(risk_factor)
        return risk_factors

class AgentPipeline:
    """Pipeline for running both AI agents in sequence."""
    
    def __init__(self):
        self.trend_researcher = TrendResearcherAgent()
        self.feedback_synthesizer = FeedbackSynthesizerAgent()
    
    async def run_full_analysis(self, posts: List[ScrapedPost]) -> tuple[TrendAnalysis, SynthesisResults]:
        """Run complete analysis pipeline."""
        logger.info("Starting full AI analysis pipeline...")
        
        # Step 1: Trend Analysis
        trend_analysis = await self.trend_researcher.analyze_trends(posts)
        logger.info(f"Trend analysis completed: {len(trend_analysis.trends)} trends identified")
        
        # Step 2: Feedback Synthesis
        synthesis_results = await self.feedback_synthesizer.synthesize_feedback(trend_analysis)
        logger.info(f"Feedback synthesis completed: {len(synthesis_results.priority_trends)} priority trends")
        
        return trend_analysis, synthesis_results

async def main():
    """Test the agents."""
    # This would be used for testing
    pass

if __name__ == "__main__":
    asyncio.run(main()) 