"""
Output handlers for K-Beauty Trend Briefing System
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from core.config import config
from core.models import DailyBriefing, CustomJSONEncoder

logger = logging.getLogger(__name__)

class OutputHandler:
    """Base class for output handlers."""
    
    def __init__(self):
        self.output_dir = config.output.output_dir
        self.output_dir.mkdir(exist_ok=True)
    
    def save_briefing(self, briefing: DailyBriefing) -> bool:
        """Save briefing in the handler's format."""
        raise NotImplementedError

class MarkdownOutputHandler(OutputHandler):
    """Handler for saving briefings in Markdown format."""
    
    def save_briefing(self, briefing: DailyBriefing) -> bool:
        """Save briefing as Markdown file."""
        try:
            # Generate markdown content
            markdown_content = briefing.to_markdown()
            
            # Create filename
            filename = f"kbeauty_briefing_{briefing.date.strftime('%Y%m%d')}.md"
            filepath = self.output_dir / filename
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Markdown briefing saved: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save markdown briefing: {e}")
            return False

class JSONOutputHandler(OutputHandler):
    """Handler for saving briefings in JSON format."""
    
    def save_briefing(self, briefing: DailyBriefing) -> bool:
        """Save briefing as JSON file."""
        try:
            # Convert to dictionary
            briefing_data = briefing.to_dict()
            
            # Create filename
            filename = f"kbeauty_briefing_{briefing.briefing_id}.json"
            filepath = self.output_dir / filename
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(briefing_data, f, indent=2, cls=CustomJSONEncoder, ensure_ascii=False)
            
            logger.info(f"JSON briefing saved: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save JSON briefing: {e}")
            return False

class NotionOutputHandler(OutputHandler):
    """Handler for saving briefings to Notion."""
    
    def __init__(self):
        super().__init__()
        self.notion_enabled = config.notion.enabled
        if self.notion_enabled:
            try:
                from notion_client import Client
                self.client = Client(auth=config.notion.token)
                self.database_id = config.notion.database_id
            except ImportError:
                logger.error("Notion client not available")
                self.notion_enabled = False
        else:
            self.client = None
            self.database_id = None
    
    def save_briefing(self, briefing: DailyBriefing) -> bool:
        """Save briefing to Notion database."""
        if not self.notion_enabled:
            logger.warning("Notion integration not enabled")
            return False
        
        try:
            # Create Notion page
            page_data = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "Title": {
                        "title": [
                            {
                                "text": {
                                    "content": f"K-Beauty Briefing - {briefing.date.strftime('%Y-%m-%d')}"
                                }
                            }
                        ]
                    },
                    "Date": {
                        "date": {
                            "start": briefing.date.isoformat()
                        }
                    },
                    "Briefing ID": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": briefing.briefing_id
                                }
                            }
                        ]
                    },
                    "Posts Analyzed": {
                        "number": briefing.scraped_posts_count
                    },
                    "Trends Identified": {
                        "number": len(briefing.trend_analysis.trends)
                    },
                    "Priority Trends": {
                        "number": len(briefing.synthesis_results.priority_trends)
                    }
                },
                "children": [
                    {
                        "object": "block",
                        "type": "heading_1",
                        "heading_1": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "Executive Summary"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": briefing.synthesis_results.executive_summary
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "Priority Trends"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
            
            # Add priority trends
            for trend in briefing.synthesis_results.priority_trends:
                page_data["children"].extend([
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"{trend.rank}. {trend.trend_name}"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"Business Impact: {trend.business_impact.value.title()}"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": trend.reasoning
                                    }
                                }
                            ]
                        }
                    }
                ])
            
            # Create the page
            response = self.client.pages.create(**page_data)
            
            logger.info(f"Notion briefing saved: {response['url']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save Notion briefing: {e}")
            return False

class OutputPipeline:
    """Pipeline for handling multiple output formats."""
    
    def __init__(self):
        self.handlers = []
        
        # Add handlers based on configuration
        if config.output.markdown_enabled:
            self.handlers.append(MarkdownOutputHandler())
        
        if config.output.json_enabled:
            self.handlers.append(JSONOutputHandler())
        
        if config.output.notion_enabled:
            self.handlers.append(NotionOutputHandler())
    
    def save_briefing(self, briefing: DailyBriefing) -> Dict[str, bool]:
        """Save briefing using all enabled handlers."""
        results = {}
        
        for handler in self.handlers:
            handler_name = handler.__class__.__name__
            success = handler.save_briefing(briefing)
            results[handler_name] = success
        
        return results
    
    def get_output_files(self, briefing: DailyBriefing) -> List[str]:
        """Get list of output files created for a briefing."""
        files = []
        
        # Check for markdown file
        if config.output.markdown_enabled:
            md_file = self.output_dir / f"kbeauty_briefing_{briefing.date.strftime('%Y%m%d')}.md"
            if md_file.exists():
                files.append(str(md_file))
        
        # Check for JSON file
        if config.output.json_enabled:
            json_file = self.output_dir / f"kbeauty_briefing_{briefing.briefing_id}.json"
            if json_file.exists():
                files.append(str(json_file))
        
        return files 