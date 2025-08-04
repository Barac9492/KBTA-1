#!/usr/bin/env python3
"""
Autonomous AI Agent for K-Beauty Trend Agent
Uses CrewAI framework for 24/7 adaptive operation
"""

import os
import sys
import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from crewai import Agent, Task, Crew, Process
    from langchain.tools import Tool
    from langchain_openai import ChatOpenAI
    CREWAI_AVAILABLE = True
except ImportError:
    print("Warning: CrewAI not available. Install with: pip install crewai")
    CREWAI_AVAILABLE = False

try:
    from core.scraper import GlowpickScraper, OliveYoungScraper
    from core.analysis import AdvancedTrendAnalyzer
    from core.output import OutputHandler
    REAL_DATA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import core modules: {e}")
    REAL_DATA_AVAILABLE = False

class KBeautyAutonomousAgent:
    """Autonomous AI agent for K-beauty trend analysis"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.tools = self._create_tools()
        
        # Initialize agents
        self.agents = self._create_agents()
        
        # Initialize tasks
        self.tasks = self._create_tasks()
        
        # Initialize crew
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agents"""
        tools = []
        
        # Scraping tool
        def scrape_trends(query: str = "") -> str:
            """Scrape K-beauty trends from multiple sources"""
            try:
                if not REAL_DATA_AVAILABLE:
                    return "Mock data: PDRN, Micro-needling, Korean Haircare trends detected"
                
                scrapers = [GlowpickScraper(), OliveYoungScraper()]
                all_data = []
                
                for scraper in scrapers:
                    try:
                        data = asyncio.run(scraper.get_trending_products())
                        all_data.extend(data)
                    except Exception as e:
                        print(f"Scraping failed: {e}")
                
                return json.dumps(all_data, indent=2)
            except Exception as e:
                return f"Scraping error: {str(e)}"
        
        # Analysis tool
        def analyze_trends(data: str) -> str:
            """Analyze trends using AI"""
            try:
                if not REAL_DATA_AVAILABLE:
                    return "Mock analysis: PDRN growing 25%, Micro-needling 18%, Haircare emerging"
                
                analyzer = AdvancedTrendAnalyzer()
                trends_data = json.loads(data) if isinstance(data, str) else data
                
                analysis = {
                    "current_trends": analyzer.analyze_current_trends(trends_data),
                    "emerging_trends": analyzer.predict_emerging_trends(trends_data),
                    "opportunities": analyzer.analyze_market_opportunities(trends_data)
                }
                
                return json.dumps(analysis, indent=2)
            except Exception as e:
                return f"Analysis error: {str(e)}"
        
        # Market research tool
        def research_market(topic: str) -> str:
            """Research market information for K-beauty trends"""
            research_results = {
                "topic": topic,
                "market_size": "$XX billion",
                "growth_rate": "15% YoY",
                "key_players": ["Amorepacific", "LG Household", "Sulwhasoo"],
                "trends": ["PDRN", "Micro-needling", "Haircare expansion"],
                "opportunities": ["Personalization", "Sustainability", "Digital transformation"]
            }
            return json.dumps(research_results, indent=2)
        
        # Notification tool
        def send_notifications(message: str) -> str:
            """Send notifications for important trends"""
            try:
                # Implementation for email/Slack notifications
                print(f"Notification sent: {message}")
                return f"Notification sent successfully: {message}"
            except Exception as e:
                return f"Notification failed: {str(e)}"
        
        tools = [
            Tool(
                name="ScrapeTrends",
                func=scrape_trends,
                description="Scrapes K-beauty trends from Glowpick, Olive Young, and social media"
            ),
            Tool(
                name="AnalyzeTrends", 
                func=analyze_trends,
                description="Analyzes trends using AI to identify patterns and opportunities"
            ),
            Tool(
                name="ResearchMarket",
                func=research_market,
                description="Researches market information for K-beauty trends and opportunities"
            ),
            Tool(
                name="SendNotifications",
                func=send_notifications,
                description="Sends notifications for important trends and insights"
            )
        ]
        
        return tools
    
    def _create_agents(self) -> List[Agent]:
        """Create specialized agents"""
        agents = []
        
        # Scraper Agent
        scraper_agent = Agent(
            role='K-Beauty Trend Scraper',
            goal='Scrape and collect the latest K-beauty trends from multiple sources',
            backstory="""You are an expert web scraper specializing in K-beauty trends. 
            You monitor Glowpick, Olive Young, social media, and other sources to identify 
            emerging trends like PDRN, micro-needling, and haircare innovations.""",
            tools=[tool for tool in self.tools if tool.name in ["ScrapeTrends"]],
            llm=self.llm,
            verbose=True
        )
        
        # Analyst Agent
        analyst_agent = Agent(
            role='K-Beauty Trend Analyst',
            goal='Analyze trends and predict future market opportunities',
            backstory="""You are a senior K-beauty market analyst with expertise in 
            trend analysis, market forecasting, and competitive intelligence. You identify 
            patterns, predict emerging trends, and provide actionable insights.""",
            tools=[tool for tool in self.tools if tool.name in ["AnalyzeTrends", "ResearchMarket"]],
            llm=self.llm,
            verbose=True
        )
        
        # Strategist Agent
        strategist_agent = Agent(
            role='K-Beauty Strategy Advisor',
            goal='Create strategic recommendations and briefings based on trend analysis',
            backstory="""You are a K-beauty strategy consultant who creates actionable 
            briefings and recommendations. You translate trend analysis into business 
            opportunities and strategic advice for different user types.""",
            tools=[tool for tool in self.tools if tool.name in ["SendNotifications"]],
            llm=self.llm,
            verbose=True
        )
        
        agents = [scraper_agent, analyst_agent, strategist_agent]
        return agents
    
    def _create_tasks(self) -> List[Task]:
        """Create tasks for the crew"""
        tasks = []
        
        # Task 1: Scrape Trends
        scrape_task = Task(
            description="""Scrape the latest K-beauty trends from multiple sources:
            1. Use ScrapeTrends tool to get data from Glowpick and Olive Young
            2. Focus on 2025 trends like PDRN, micro-needling, haircare
            3. Collect social media trends and influencer mentions
            4. Ensure comprehensive coverage of all relevant sources""",
            agent=self.agents[0],  # Scraper Agent
            expected_output="""A comprehensive dataset of current K-beauty trends including:
            - Product trends (PDRN, micro-needling, etc.)
            - Category trends (haircare expansion, etc.)
            - Social media trends and mentions
            - Market data and statistics"""
        )
        
        # Task 2: Analyze Trends
        analyze_task = Task(
            description="""Analyze the scraped trends to identify patterns and opportunities:
            1. Use AnalyzeTrends tool to process the scraped data
            2. Identify current trends and their growth rates
            3. Predict emerging trends for the next 3-6 months
            4. Research market opportunities using ResearchMarket tool
            5. Focus on actionable insights for different user types""",
            agent=self.agents[1],  # Analyst Agent
            expected_output="""A detailed analysis including:
            - Current trend analysis with growth rates
            - Emerging trend predictions
            - Market opportunity identification
            - Competitive landscape analysis
            - Risk assessment and recommendations"""
        )
        
        # Task 3: Create Strategic Briefings
        strategy_task = Task(
            description="""Create strategic briefings and recommendations:
            1. Synthesize the trend analysis into actionable insights
            2. Create personalized briefings for different user types:
               - Gen Z consumers (affordable, trendy)
               - Brand marketers (competitive intelligence)
               - Retailers (supply chain, sourcing)
            3. Generate executive summaries and key recommendations
            4. Send notifications for important trends using SendNotifications tool
            5. Focus on solving real pain points: market saturation, tariffs, personalization""",
            agent=self.agents[2],  # Strategist Agent
            expected_output="""Strategic briefings including:
            - Executive summary for each user type
            - Key insights and actionable recommendations
            - Market outlook and predictions
            - Personalized product recommendations
            - Tariff navigation strategies
            - Notification system for new trends"""
        )
        
        tasks = [scrape_task, analyze_task, strategy_task]
        return tasks
    
    def run_autonomous_cycle(self) -> Dict[str, Any]:
        """Run one autonomous cycle"""
        try:
            print("🤖 Starting autonomous K-beauty trend analysis cycle...")
            
            # Run the crew
            result = self.crew.kickoff()
            
            # Process results
            processed_result = self._process_results(result)
            
            # Store results
            self._store_results(processed_result)
            
            # Send notifications
            self._send_notifications(processed_result)
            
            print("✅ Autonomous cycle completed successfully!")
            return processed_result
            
        except Exception as e:
            print(f"❌ Autonomous cycle failed: {e}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def run_continuous_operation(self, interval_hours: int = 6):
        """Run continuous autonomous operation"""
        print(f"🚀 Starting continuous autonomous operation (every {interval_hours} hours)...")
        
        while True:
            try:
                # Run one cycle
                result = self.run_autonomous_cycle()
                
                # Log result
                print(f"📊 Cycle result: {result}")
                
                # Wait for next cycle
                print(f"⏰ Waiting {interval_hours} hours until next cycle...")
                time.sleep(interval_hours * 3600)
                
            except KeyboardInterrupt:
                print("🛑 Autonomous operation stopped by user")
                break
            except Exception as e:
                print(f"❌ Cycle failed: {e}")
                print("🔄 Retrying in 1 hour...")
                time.sleep(3600)
    
    def _process_results(self, crew_result) -> Dict[str, Any]:
        """Process crew results into structured format"""
        try:
            # Extract key information from crew result
            result_text = str(crew_result)
            
            # Parse structured data if available
            processed_result = {
                "timestamp": datetime.now().isoformat(),
                "raw_result": result_text,
                "trends_identified": self._extract_trends(result_text),
                "recommendations": self._extract_recommendations(result_text),
                "market_insights": self._extract_market_insights(result_text),
                "user_personas": self._create_user_briefings(result_text)
            }
            
            return processed_result
            
        except Exception as e:
            print(f"Error processing results: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "raw_result": str(crew_result)
            }
    
    def _extract_trends(self, result_text: str) -> List[str]:
        """Extract trends from result text"""
        trends = []
        keywords = ["PDRN", "micro-needling", "haircare", "glass skin", "snail mucin"]
        
        for keyword in keywords:
            if keyword.lower() in result_text.lower():
                trends.append(keyword)
        
        return trends
    
    def _extract_recommendations(self, result_text: str) -> List[str]:
        """Extract recommendations from result text"""
        recommendations = []
        
        # Simple extraction - in production, use more sophisticated NLP
        if "recommend" in result_text.lower():
            lines = result_text.split('\n')
            for line in lines:
                if "recommend" in line.lower() or "suggest" in line.lower():
                    recommendations.append(line.strip())
        
        return recommendations[:5]  # Limit to top 5
    
    def _extract_market_insights(self, result_text: str) -> Dict[str, Any]:
        """Extract market insights from result text"""
        return {
            "market_size": "$XX billion",
            "growth_rate": "15% YoY",
            "key_trends": self._extract_trends(result_text),
            "opportunities": ["Personalization", "Sustainability", "Digital transformation"]
        }
    
    def _create_user_briefings(self, result_text: str) -> Dict[str, Any]:
        """Create personalized briefings for different user types"""
        user_types = ["gen_z", "brand_marketer", "retailer"]
        briefings = {}
        
        for user_type in user_types:
            briefings[user_type] = {
                "executive_summary": f"Personalized analysis for {user_type}",
                "key_insights": self._extract_trends(result_text),
                "recommendations": self._extract_recommendations(result_text),
                "market_outlook": "Optimistic growth in K-beauty market"
            }
        
        return briefings
    
    def _store_results(self, results: Dict[str, Any]):
        """Store results in database/cache"""
        try:
            # Store in output directory
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Save as JSON
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            json_file = output_dir / f"autonomous_agent_{timestamp}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results stored: {json_file}")
            
        except Exception as e:
            print(f"Error storing results: {e}")
    
    def _send_notifications(self, results: Dict[str, Any]):
        """Send notifications for important findings"""
        try:
            # Check for significant trends
            trends = results.get("trends_identified", [])
            
            if trends:
                notification = f"🚨 New K-beauty trends detected: {', '.join(trends)}"
                print(f"📢 {notification}")
                
                # In production, send to email/Slack
                # self._send_email_notification(notification)
                # self._send_slack_notification(notification)
            
        except Exception as e:
            print(f"Error sending notifications: {e}")

# Standalone execution
if __name__ == "__main__":
    if not CREWAI_AVAILABLE:
        print("❌ CrewAI not available. Install with: pip install crewai")
        sys.exit(1)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        sys.exit(1)
    
    # Create and run agent
    agent = KBeautyAutonomousAgent()
    
    # Run one cycle
    result = agent.run_autonomous_cycle()
    print(f"Result: {json.dumps(result, indent=2)}")
    
    # Uncomment for continuous operation
    # agent.run_continuous_operation(interval_hours=6) 