"""
Configuration management for K-Beauty Trend Briefing System
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ScrapingConfig:
    """Configuration for web scraping."""
    delay_between_requests: float = 2.0
    max_posts_per_source: int = 50
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    headless: bool = True
    timeout: int = 30000

@dataclass
class LLMConfig:
    """Configuration for LLM services."""
    model: str = "gpt-4"
    max_tokens: int = 2000
    temperature: float = 0.3
    openai_api_key: Optional[str] = None

@dataclass
class NotionConfig:
    """Configuration for Notion integration."""
    token: Optional[str] = None
    database_id: Optional[str] = None
    enabled: bool = False

@dataclass
class OutputConfig:
    """Configuration for output formats."""
    markdown_enabled: bool = True
    notion_enabled: bool = False
    json_enabled: bool = True
    output_dir: Path = Path("output")

@dataclass
class PipelineConfig:
    """Configuration for the daily pipeline."""
    auto_run: bool = False
    schedule_time: str = "09:00"  # Daily run time
    retention_days: int = 30
    max_daily_runs: int = 3

class Config:
    """Main configuration class."""
    
    def __init__(self, validate_api_keys: bool = True):
        self.scraping = ScrapingConfig()
        self.llm = LLMConfig()
        self.notion = NotionConfig()
        self.output = OutputConfig()
        self.pipeline = PipelineConfig()
        
        self._load_from_env()
        
        if validate_api_keys:
            self._validate_config()
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        # OpenAI Configuration
        self.llm.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.llm.model = os.getenv("ANALYSIS_MODEL", "gpt-4")
        self.llm.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        self.llm.temperature = float(os.getenv("TEMPERATURE", "0.3"))
        
        # Notion Configuration
        self.notion.token = os.getenv("NOTION_TOKEN", "")
        self.notion.database_id = os.getenv("NOTION_DATABASE_ID", "")
        self.notion.enabled = bool(self.notion.token and self.notion.database_id)
        
        # Scraping Configuration
        self.scraping.delay_between_requests = float(os.getenv("SCRAPING_DELAY", "2"))
        self.scraping.max_posts_per_source = int(os.getenv("MAX_POSTS_PER_SOURCE", "50"))
        
        # Pipeline Configuration
        self.pipeline.schedule_time = os.getenv("SCHEDULE_TIME", "06:00")
        self.pipeline.auto_run = os.getenv("AUTO_RUN", "false").lower() == "true"
        self.pipeline.retention_days = int(os.getenv("RETENTION_DAYS", "30"))
        
        # Output Configuration
        self.output.markdown_enabled = os.getenv("MARKDOWN_ENABLED", "true").lower() == "true"
        self.output.json_enabled = os.getenv("JSON_ENABLED", "true").lower() == "true"
        
        # Use /tmp for Vercel compatibility (read-only filesystem)
        if os.getenv("VERCEL"):
            self.output.output_dir = Path("/tmp")
        else:
            self.output.output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
            # Only try to create directory if not on Vercel
            try:
                self.output.output_dir.mkdir(exist_ok=True)
            except OSError:
                # Fallback to /tmp if we can't create the directory
                self.output.output_dir = Path("/tmp")
    
    def _validate_config(self):
        """Validate configuration settings."""
        if not self.llm.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required")
        
        if self.notion.enabled and not (self.notion.token and self.notion.database_id):
            raise ValueError("Notion integration requires both NOTION_TOKEN and NOTION_DATABASE_ID")
    
    def get_sources_config(self) -> Dict:
        """Get scraping sources configuration."""
        return {
            "naver_beauty": {
                "urls": [
                    "https://search.naver.com/search.naver?where=view&query=K뷰티+트렌드",
                    "https://search.naver.com/search.naver?where=view&query=한국화장품+리뷰",
                    "https://search.naver.com/search.naver?where=view&query=K뷰티+신상품",
                ],
                "selectors": {
                    "posts": "li.bx, div.total_wrap, div.thumb",
                    "title": "a.title_link, h3.title, a.link_tit",
                    "content": "div.dsc, div.content, p.content",
                    "date": "span.date, time, span.time",
                    "author": "span.author, a.author, span.writer"
                }
            },
            "instagram_beauty": {
                "hashtags": [
                    "#kbeauty", "#koreanbeauty", "#koreanskincare",
                    "#kbeautytrends", "#koreanmakeup", "#koreancosmetics",
                    "#kbeautyproducts", "#koreanskincare", "#koreanbeautytips"
                ]
            },
            "youtube_beauty": {
                "channels": [
                    "https://www.youtube.com/results?search_query=korean+beauty+trends",
                    "https://www.youtube.com/results?search_query=korean+skincare+reviews",
                    "https://www.youtube.com/results?search_query=kbeauty+new+products"
                ]
            }
        }

# Global configuration instance - don't validate API keys for help commands
config = Config(validate_api_keys=False) 