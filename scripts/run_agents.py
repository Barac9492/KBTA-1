#!/usr/bin/env python3
"""
K-Beauty Trend Agent Runner
Reads scraped content and routes through LLMs for trend analysis and synthesis.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import asyncio

import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TrendAgentRunner:
    """Runs trend research and synthesis agents using LLMs."""
    
    def __init__(self):
        self.data_dir = Path("data")
        self.agents_dir = Path("agents")
        
        # Initialize OpenAI client
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Load agent prompts
        self.trend_researcher_prompt = self.load_agent_prompt("trend-researcher.md")
        self.feedback_synthesizer_prompt = self.load_agent_prompt("feedback-synthesizer.md")
        
        self.scraped_data = []
        self.trend_analysis = {}
        self.synthesis_results = {}
        
    def load_agent_prompt(self, filename: str) -> str:
        """Load agent prompt from markdown file."""
        prompt_file = self.agents_dir / filename
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Agent prompt file not found: {prompt_file}")
            return ""
    
    def load_scraped_data(self) -> bool:
        """Load scraped content from JSON file."""
        scraped_file = self.data_dir / "scraped_content.json"
        
        try:
            with open(scraped_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.scraped_data = data.get("posts", [])
                logger.info(f"Loaded {len(self.scraped_data)} scraped posts")
                return True
        except FileNotFoundError:
            logger.error(f"Scraped data file not found: {scraped_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing scraped data: {e}")
            return False
    
    def prepare_content_for_analysis(self) -> str:
        """Prepare scraped content for LLM analysis."""
        if not self.scraped_data:
            return "No scraped content available for analysis."
        
        # Format content for analysis
        formatted_content = []
        
        for i, post in enumerate(self.scraped_data[:50]):  # Limit to 50 posts for analysis
            formatted_post = f"""
Post {i+1}:
Title: {post.get('title', 'No title')}
Content: {post.get('content', 'No content')}
Source: {post.get('source', 'Unknown')}
Date: {post.get('date', 'Unknown date')}
URL: {post.get('url', 'No URL')}
"""
            formatted_content.append(formatted_post)
        
        return "\n".join(formatted_content)
    
    async def run_trend_researcher(self, content: str) -> Dict:
        """Run the trend researcher agent."""
        logger.info("Running trend researcher agent...")
        
        # Prepare the prompt with content
        full_prompt = f"""
{self.trend_researcher_prompt}

Please analyze the following K-beauty content and identify trends:

{content}

Provide your analysis in the specified JSON format.
"""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert K-beauty trend researcher."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract and parse JSON response
            response_text = response.choices[0].message.content
            self.trend_analysis = self.parse_json_response(response_text)
            
            logger.info("Trend researcher analysis completed")
            return self.trend_analysis
            
        except Exception as e:
            logger.error(f"Error running trend researcher: {e}")
            return {}
    
    async def run_feedback_synthesizer(self, trend_analysis: Dict) -> Dict:
        """Run the feedback synthesizer agent."""
        logger.info("Running feedback synthesizer agent...")
        
        # Prepare trend analysis for synthesis
        analysis_text = json.dumps(trend_analysis, indent=2, ensure_ascii=False)
        
        full_prompt = f"""
{self.feedback_synthesizer_prompt}

Please synthesize the following trend analysis into actionable business intelligence:

{analysis_text}

Provide your synthesis in the specified JSON format.
"""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert K-beauty trend synthesizer."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract and parse JSON response
            response_text = response.choices[0].message.content
            self.synthesis_results = self.parse_json_response(response_text)
            
            logger.info("Feedback synthesizer analysis completed")
            return self.synthesis_results
            
        except Exception as e:
            logger.error(f"Error running feedback synthesizer: {e}")
            return {}
    
    def parse_json_response(self, response_text: str) -> Dict:
        """Parse JSON response from LLM."""
        try:
            # Try to extract JSON from the response
            import re
            
            # Look for JSON blocks in the response
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find JSON without markdown formatting
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    json_str = response_text
            
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Could not parse JSON response: {e}")
            logger.warning(f"Raw response: {response_text[:500]}...")
            return {"error": "Failed to parse JSON response", "raw_response": response_text[:500]}
    
    def save_results(self):
        """Save analysis results to JSON file."""
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "scraped_posts_count": len(self.scraped_data),
            "trend_analysis": self.trend_analysis,
            "synthesis_results": self.synthesis_results
        }
        
        output_file = self.data_dir / "latest_trends.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    async def run_full_analysis(self):
        """Run the complete trend analysis pipeline."""
        logger.info("Starting K-beauty trend analysis pipeline...")
        
        # Load scraped data
        if not self.load_scraped_data():
            logger.error("Failed to load scraped data. Please run the scraper first.")
            return
        
        # Prepare content for analysis
        content = self.prepare_content_for_analysis()
        
        if not content or content == "No scraped content available for analysis.":
            logger.error("No content available for analysis.")
            return
        
        # Run trend researcher
        trend_analysis = await self.run_trend_researcher(content)
        
        if not trend_analysis:
            logger.error("Trend analysis failed.")
            return
        
        # Run feedback synthesizer
        synthesis_results = await self.run_feedback_synthesizer(trend_analysis)
        
        if not synthesis_results:
            logger.error("Synthesis failed.")
            return
        
        # Save results
        self.save_results()
        
        logger.info("Trend analysis pipeline completed successfully!")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print a summary of the analysis results."""
        print("\n" + "="*50)
        print("K-BEAUTY TREND ANALYSIS SUMMARY")
        print("="*50)
        
        if self.trend_analysis.get("trends"):
            print(f"\n📊 Trends Identified: {len(self.trend_analysis['trends'])}")
            for trend in self.trend_analysis["trends"][:5]:  # Show top 5
                print(f"  • {trend.get('trend_name', 'Unknown trend')}")
        
        if self.synthesis_results.get("priority_trends"):
            print(f"\n🎯 Priority Trends: {len(self.synthesis_results['priority_trends'])}")
            for trend in self.synthesis_results["priority_trends"][:3]:  # Show top 3
                print(f"  • {trend.get('trend_name', 'Unknown trend')} (Impact: {trend.get('business_impact', 'Unknown')})")
        
        if self.synthesis_results.get("market_opportunities"):
            print(f"\n💡 Market Opportunities: {len(self.synthesis_results['market_opportunities'])}")
        
        print("\n" + "="*50)

async def main():
    """Main function to run the agent pipeline."""
    runner = TrendAgentRunner()
    await runner.run_full_analysis()

if __name__ == "__main__":
    asyncio.run(main()) 