#!/usr/bin/env python3
"""
K-Beauty Trend Notion Integration
Sends trend analysis results to Notion database for easy access and collaboration.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os

from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotionTrendPublisher:
    """Publishes trend analysis results to Notion database."""
    
    def __init__(self):
        self.data_dir = Path("data")
        
        # Initialize Notion client
        notion_token = os.getenv("NOTION_TOKEN")
        database_id = os.getenv("NOTION_DATABASE_ID")
        
        if not notion_token:
            raise ValueError("NOTION_TOKEN not found in environment variables")
        if not database_id:
            raise ValueError("NOTION_DATABASE_ID not found in environment variables")
        
        self.notion = Client(auth=notion_token)
        self.database_id = database_id
        
        self.trend_data = {}
        
    def load_trend_data(self) -> bool:
        """Load trend analysis results from JSON file."""
        trends_file = self.data_dir / "latest_trends.json"
        
        try:
            with open(trends_file, 'r', encoding='utf-8') as f:
                self.trend_data = json.load(f)
                logger.info("Loaded trend analysis data")
                return True
        except FileNotFoundError:
            logger.error(f"Trend data file not found: {trends_file}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing trend data: {e}")
            return False
    
    def create_trend_page(self, trend: Dict) -> Optional[str]:
        """Create a Notion page for a single trend."""
        try:
            # Prepare page properties
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": trend.get("trend_name", "Unknown Trend")
                            }
                        }
                    ]
                },
                "Category": {
                    "select": {
                        "name": trend.get("category", "skincare").title()
                    }
                },
                "Trend Type": {
                    "select": {
                        "name": trend.get("trend_type", "emerging").title()
                    }
                },
                "Confidence": {
                    "number": trend.get("confidence", 0.5)
                },
                "Price Range": {
                    "select": {
                        "name": trend.get("price_range", "mid-range").replace("-", " ").title()
                    }
                },
                "Seasonal Factors": {
                    "multi_select": [
                        {"name": factor.title()} for factor in trend.get("seasonal_factors", "year-round").split("|")
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Active"
                    }
                },
                "Last Updated": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }
            
            # Prepare page content
            children = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Trend Description"
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
                                    "content": trend.get("description", "No description available.")
                                }
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Target Demographic"
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
                                    "content": trend.get("target_demographic", "Not specified.")
                                }
                            }
                        ]
                    }
                }
            ]
            
            # Add evidence links if available
            if trend.get("evidence"):
                children.extend([
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "Evidence Sources"
                                    }
                                }
                            ]
                        }
                    }
                ])
                
                for evidence in trend.get("evidence", [])[:5]:  # Limit to 5 sources
                    children.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": evidence
                                    }
                                }
                            ]
                        }
                    })
            
            # Create the page
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )
            
            logger.info(f"Created Notion page for trend: {trend.get('trend_name')}")
            return response["id"]
            
        except Exception as e:
            logger.error(f"Error creating Notion page for trend {trend.get('trend_name')}: {e}")
            return None
    
    def create_synthesis_page(self, synthesis_data: Dict) -> Optional[str]:
        """Create a Notion page for synthesis results."""
        try:
            # Prepare page properties
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"K-Beauty Trend Synthesis - {datetime.now().strftime('%Y-%m-%d')}"
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": "Synthesis Report"
                    }
                },
                "Status": {
                    "select": {
                        "name": "Active"
                    }
                },
                "Last Updated": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                }
            }
            
            # Prepare page content
            children = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
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
                                    "content": synthesis_data.get("executive_summary", "No summary available.")
                                }
                            }
                        ]
                    }
                }
            ]
            
            # Add priority trends
            if synthesis_data.get("priority_trends"):
                children.extend([
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
                ])
                
                for trend in synthesis_data.get("priority_trends", []):
                    children.extend([
                        {
                            "object": "block",
                            "type": "heading_3",
                            "heading_3": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": f"{trend.get('rank', 'N/A')}. {trend.get('trend_name', 'Unknown')}"
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
                                            "content": f"Business Impact: {trend.get('business_impact', 'Unknown')} | Time to Market: {trend.get('time_to_market', 'Unknown')}"
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
                                            "content": f"Target Audience: {trend.get('target_audience', 'Not specified')}"
                                        }
                                    }
                                ]
                            }
                        }
                    ])
                    
                    # Add recommendations
                    if trend.get("recommendations"):
                        children.append({
                            "object": "block",
                            "type": "heading_4",
                            "heading_4": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": "Recommendations"
                                        }
                                    }
                                ]
                            }
                        })
                        
                        for rec in trend.get("recommendations", []):
                            children.append({
                                "object": "block",
                                "type": "bulleted_list_item",
                                "bulleted_list_item": {
                                    "rich_text": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": rec
                                            }
                                        }
                                    ]
                                }
                            })
            
            # Add market opportunities
            if synthesis_data.get("market_opportunities"):
                children.extend([
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "Market Opportunities"
                                    }
                                }
                            ]
                        }
                    }
                ])
                
                for opportunity in synthesis_data.get("market_opportunities", []):
                    children.extend([
                        {
                            "object": "block",
                            "type": "heading_3",
                            "heading_3": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": opportunity.get("opportunity", "Unknown opportunity")
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
                                            "content": f"Size: {opportunity.get('size', 'Unknown')} | Barriers: {opportunity.get('barriers', 'None identified')}"
                                        }
                                    }
                                ]
                            }
                        }
                    ])
            
            # Create the page
            response = self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )
            
            logger.info("Created Notion page for trend synthesis")
            return response["id"]
            
        except Exception as e:
            logger.error(f"Error creating Notion synthesis page: {e}")
            return None
    
    def publish_to_notion(self):
        """Publish all trend data to Notion."""
        logger.info("Starting Notion publication...")
        
        # Load trend data
        if not self.load_trend_data():
            logger.error("Failed to load trend data.")
            return
        
        published_pages = []
        
        # Publish individual trends
        trend_analysis = self.trend_data.get("trend_analysis", {})
        if trend_analysis.get("trends"):
            logger.info(f"Publishing {len(trend_analysis['trends'])} trends to Notion...")
            
            for trend in trend_analysis["trends"]:
                page_id = self.create_trend_page(trend)
                if page_id:
                    published_pages.append(page_id)
        
        # Publish synthesis results
        synthesis_results = self.trend_data.get("synthesis_results", {})
        if synthesis_results:
            logger.info("Publishing synthesis results to Notion...")
            synthesis_page_id = self.create_synthesis_page(synthesis_results)
            if synthesis_page_id:
                published_pages.append(synthesis_page_id)
        
        logger.info(f"Successfully published {len(published_pages)} pages to Notion")
        
        # Print summary
        self.print_publication_summary(published_pages)
    
    def print_publication_summary(self, published_pages: List[str]):
        """Print a summary of the publication results."""
        print("\n" + "="*50)
        print("NOTION PUBLICATION SUMMARY")
        print("="*50)
        
        trend_analysis = self.trend_data.get("trend_analysis", {})
        synthesis_results = self.trend_data.get("synthesis_results", {})
        
        print(f"\n📊 Trends Published: {len(trend_analysis.get('trends', []))}")
        print(f"📋 Synthesis Report: {'✅' if synthesis_results else '❌'}")
        print(f"📄 Total Pages Created: {len(published_pages)}")
        
        if trend_analysis.get("trends"):
            print(f"\n🎯 Top Trends:")
            for trend in trend_analysis["trends"][:3]:
                print(f"  • {trend.get('trend_name', 'Unknown')} ({trend.get('category', 'Unknown')})")
        
        print("\n" + "="*50)

def main():
    """Main function to run the Notion publisher."""
    try:
        publisher = NotionTrendPublisher()
        publisher.publish_to_notion()
    except Exception as e:
        logger.error(f"Error in Notion publication: {e}")

if __name__ == "__main__":
    main() 