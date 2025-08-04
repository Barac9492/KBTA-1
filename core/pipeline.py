"""
Main pipeline orchestrator for K-Beauty Daily Trend Briefing System
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

from core.config import config
from core.models import DailyBriefing, PipelineStatus, ScrapedPost
from core.scraper import KBeautyScraper
from core.agents import AgentPipeline
from core.output import OutputPipeline

logger = logging.getLogger(__name__)

class DailyBriefingPipeline:
    """Main pipeline for daily K-beauty trend briefings."""
    
    def __init__(self):
        self.scraper = KBeautyScraper()
        self.agent_pipeline = AgentPipeline()
        self.output_pipeline = OutputPipeline()
        self.status = PipelineStatus(
            status="idle",
            start_time=datetime.now()
        )
    
    def _validate_api_keys(self):
        """Validate API keys before running pipeline."""
        if not config.llm.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required to run the briefing pipeline")
        
        if config.notion.enabled and not (config.notion.token and config.notion.database_id):
            raise ValueError("Notion integration requires both NOTION_TOKEN and NOTION_DATABASE_ID")
    
    async def run_daily_briefing(self) -> Optional[DailyBriefing]:
        """Run the complete daily briefing pipeline."""
        logger.info("Starting daily K-beauty briefing pipeline...")
        
        # Validate API keys before starting
        self._validate_api_keys()
        
        # Update status
        self.status = PipelineStatus(
            status="running",
            start_time=datetime.now()
        )
        
        try:
            # Step 1: Scrape content
            logger.info("Step 1: Scraping K-beauty content...")
            posts = await self.scraper.scrape_all_sources()
            
            if not posts:
                logger.error("No content scraped, aborting pipeline")
                self._update_status("failed", "No content scraped")
                return None
            
            logger.info(f"Scraped {len(posts)} relevant posts")
            
            # Step 2: Run AI analysis
            logger.info("Step 2: Running AI trend analysis...")
            trend_analysis, synthesis_results = await self.agent_pipeline.run_full_analysis(posts)
            
            if not trend_analysis or not synthesis_results:
                logger.error("AI analysis failed, aborting pipeline")
                self._update_status("failed", "AI analysis failed")
                return None
            
            logger.info(f"Identified {len(trend_analysis.trends)} trends")
            logger.info(f"Generated {len(synthesis_results.priority_trends)} priority trends")
            
            # Step 3: Create briefing
            logger.info("Step 3: Creating daily briefing...")
            briefing_id = f"briefing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            briefing = DailyBriefing(
                briefing_id=briefing_id,
                date=datetime.now(),
                scraped_posts_count=len(posts),
                trend_analysis=trend_analysis,
                synthesis_results=synthesis_results
            )
            
            # Step 4: Save outputs
            logger.info("Step 4: Saving briefing outputs...")
            output_results = self.output_pipeline.save_briefing(briefing)
            
            # Log output results
            for handler_name, success in output_results.items():
                if success:
                    logger.info(f"✅ {handler_name}: Success")
                else:
                    logger.warning(f"⚠️ {handler_name}: Failed")
            
            # Update status
            self._update_status("completed", briefing_id=briefing.briefing_id)
            
            logger.info("Daily briefing pipeline completed successfully!")
            return briefing
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self._update_status("failed", str(e))
            return None
    
    def _update_status(self, status: str, error_message: Optional[str] = None, briefing_id: Optional[str] = None):
        """Update pipeline status."""
        self.status.status = status
        self.status.end_time = datetime.now()
        self.status.error_message = error_message
        self.status.briefing_id = briefing_id
    
    def get_status(self) -> PipelineStatus:
        """Get current pipeline status."""
        return self.status
    
    def get_latest_briefing(self) -> Optional[DailyBriefing]:
        """Get the most recent briefing from output files."""
        try:
            # Look for the most recent JSON briefing file
            output_dir = config.output.output_dir
            briefing_files = list(output_dir.glob("kbeauty_briefing_*.json"))
            
            if not briefing_files:
                return None
            
            # Get the most recent file
            latest_file = max(briefing_files, key=lambda f: f.stat().st_mtime)
            
            # Load the briefing
            with open(latest_file, 'r', encoding='utf-8') as f:
                import json
                data = json.load(f)
            
            # Convert back to DailyBriefing object
            # This is a simplified conversion - in production you'd want a proper deserializer
            return data
            
        except Exception as e:
            logger.error(f"Error loading latest briefing: {e}")
            return None
    
    def cleanup_old_files(self, retention_days: int = None):
        """Clean up old briefing files."""
        if retention_days is None:
            retention_days = config.pipeline.retention_days
        
        try:
            output_dir = config.output.output_dir
            cutoff_date = datetime.now().timestamp() - (retention_days * 24 * 60 * 60)
            
            # Find old files
            old_files = []
            for file in output_dir.glob("kbeauty_briefing_*"):
                if file.stat().st_mtime < cutoff_date:
                    old_files.append(file)
            
            # Delete old files
            for file in old_files:
                file.unlink()
                logger.info(f"Deleted old file: {file}")
            
            logger.info(f"Cleaned up {len(old_files)} old briefing files")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

class PipelineScheduler:
    """Scheduler for automated daily briefings."""
    
    def __init__(self):
        self.pipeline = DailyBriefingPipeline()
        self.is_running = False
    
    async def start_scheduler(self):
        """Start the automated scheduler."""
        logger.info("Starting automated briefing scheduler...")
        self.is_running = True
        
        while self.is_running:
            try:
                # Check if it's time to run
                current_time = datetime.now()
                schedule_time = datetime.strptime(config.pipeline.schedule_time, "%H:%M").time()
                
                if current_time.time() >= schedule_time:
                    # Run the pipeline
                    logger.info("Running scheduled daily briefing...")
                    briefing = await self.pipeline.run_daily_briefing()
                    
                    if briefing:
                        logger.info("Scheduled briefing completed successfully")
                    else:
                        logger.error("Scheduled briefing failed")
                
                # Wait until next day
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    def stop_scheduler(self):
        """Stop the automated scheduler."""
        logger.info("Stopping automated briefing scheduler...")
        self.is_running = False

async def main():
    """Main function to run the pipeline."""
    pipeline = DailyBriefingPipeline()
    
    # Run the pipeline
    briefing = await pipeline.run_daily_briefing()
    
    if briefing:
        print(f"✅ Daily briefing completed: {briefing.briefing_id}")
        print(f"📊 Trends identified: {len(briefing.trend_analysis.trends)}")
        print(f"🎯 Priority trends: {len(briefing.synthesis_results.priority_trends)}")
        print(f"💡 Market opportunities: {len(briefing.synthesis_results.market_opportunities)}")
    else:
        print("❌ Daily briefing failed")

if __name__ == "__main__":
    asyncio.run(main()) 