from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.config import Config
    from core.pipeline import Pipeline
    from core.models import DailyBriefing
    from core.output import OutputHandler
    REAL_DATA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import core modules: {e}")
    REAL_DATA_AVAILABLE = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if self.path == '/api/health':
            response = {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
                "real_data_available": REAL_DATA_AVAILABLE
            }
        elif self.path == '/api/test':
            response = {
                "status": "success",
                "message": "API is working!",
                "timestamp": datetime.now().isoformat()
            }
        elif self.path == '/api/latest':
            # Try to get real data first, fallback to mock data
            if REAL_DATA_AVAILABLE:
                try:
                    # Initialize the pipeline
                    config = Config()
                    pipeline = Pipeline(config)
                    output_handler = OutputHandler()
                    
                    # Get the latest briefing from output directory
                    latest_briefing = pipeline.get_latest_briefing()
                    
                    if latest_briefing:
                        # Convert the briefing to the expected format
                        response = {
                            "status": "success",
                            "data": {
                                "briefing_id": latest_briefing.get("briefing_id", "real_briefing_001"),
                                "date": latest_briefing.get("date", datetime.now().isoformat()),
                                "scraped_posts_count": latest_briefing.get("scraped_posts_count", 0),
                                "trend_analysis": latest_briefing.get("trend_analysis", {
                                    "trends": []
                                }),
                                "synthesis_results": latest_briefing.get("synthesis_results", {
                                    "executive_summary": "No analysis available yet.",
                                    "key_insights": [],
                                    "actionable_recommendations": [],
                                    "market_outlook": "No market outlook available."
                                })
                            }
                        }
                    else:
                        # No real data available, use mock data
                        response = self._get_mock_response()
                except Exception as e:
                    print(f"Error getting real data: {e}")
                    response = self._get_mock_response()
            else:
                # Core modules not available, use mock data
                response = self._get_mock_response()
        elif self.path == '/api/briefings':
            # Return list of available briefings
            try:
                # Try to read from output directory first
                output_dir = Path(__file__).parent.parent / "output"
                briefings = []
                
                if output_dir.exists():
                    json_files = list(output_dir.glob("*.json"))
                    if json_files:
                        for json_file in json_files:
                            try:
                                with open(json_file, 'r', encoding='utf-8') as f:
                                    briefing_data = json.load(f)
                                
                                briefings.append({
                                    "briefing_id": briefing_data.get("briefing_id", "unknown"),
                                    "title": f"K-Beauty Trend Briefing - {briefing_data.get('date', 'Unknown Date')}",
                                    "date": briefing_data.get("date", datetime.now().isoformat()),
                                    "summary": briefing_data.get("synthesis_results", {}).get("executive_summary", "No summary available"),
                                    "trend_count": len(briefing_data.get("trend_analysis", {}).get("trends", [])),
                                    "source_count": briefing_data.get("scraped_posts_count", 0),
                                    "category": "GENERAL",
                                    "categories": ["K-Beauty", "Trend Analysis"]
                                })
                            except Exception as e:
                                print(f"Error reading briefing file {json_file}: {e}")
                                continue
                
                # If no real data, provide sample briefings
                if not briefings:
                    briefings = [
                        {
                            "briefing_id": "briefing_20250801",
                            "title": "K-Beauty Trend Briefing - 2025-08-01T05:00:00",
                            "date": "2025-08-01T05:00:00",
                            "summary": "K-beauty continues to innovate with PDRN and micro-needling technologies.",
                            "trend_count": 2,
                            "source_count": 12,
                            "category": "GENERAL",
                            "categories": ["K-Beauty", "Trend Analysis"]
                        },
                        {
                            "briefing_id": "briefing_20250730",
                            "title": "K-Beauty Trend Briefing - 2025-07-30T05:00:00",
                            "date": "2025-07-30T05:00:00",
                            "summary": "Korean haircare emerges as the next big category while glass skin remains popular.",
                            "trend_count": 2,
                            "source_count": 8,
                            "category": "GENERAL",
                            "categories": ["K-Beauty", "Trend Analysis"]
                        },
                        {
                            "briefing_id": "briefing_20250728",
                            "title": "K-Beauty Trend Briefing - 2025-07-28T05:00:00",
                            "date": "2025-07-28T05:00:00",
                            "summary": "Natural ingredients like propolis are becoming mainstream while cushion foundations evolve.",
                            "trend_count": 2,
                            "source_count": 15,
                            "category": "GENERAL",
                            "categories": ["K-Beauty", "Trend Analysis"]
                        }
                    ]
                
                response = {
                    "status": "success",
                    "data": briefings
                }
            except Exception as e:
                print(f"Error getting briefings: {e}")
                response = {
                    "status": "success",
                    "data": []
                }
        elif self.path == '/api/trigger':
            # Handle trigger request
            if REAL_DATA_AVAILABLE:
                try:
                    # Initialize the pipeline
                    config = Config()
                    pipeline = Pipeline(config)
                    
                    # Run the analysis (this will take some time)
                    result = pipeline.run_analysis()
                    
                    response = {
                        "status": "success",
                        "message": "Analysis completed successfully",
                        "briefing_id": result.get("briefing_id", "new_briefing"),
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    print(f"Error running analysis: {e}")
                    response = {
                        "status": "error",
                        "message": f"Failed to run analysis: {str(e)}"
                    }
            else:
                response = {
                    "status": "error",
                    "message": "Real analysis not available - using mock data"
                }
        else:
            response = {
                "message": "K-Beauty Daily Trend Briefing API",
                "version": "2.0.0",
                "endpoints": {
                    "health": "GET /api/health - Health check",
                    "test": "GET /api/test - Test endpoint",
                    "latest": "GET /api/latest - Get latest briefing",
                    "trigger": "POST /api/trigger - Run new analysis"
                }
            }
        
        self.wfile.write(json.dumps(response).encode())
        return

    def _get_mock_response(self):
        """Return test data from output directory or fallback to mock data."""
        try:
            # Try to read from output directory
            output_dir = Path(__file__).parent.parent / "output"
            if output_dir.exists():
                # Find the latest JSON file
                json_files = list(output_dir.glob("*.json"))
                if json_files:
                    # Get the most recent file
                    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        briefing_data = json.load(f)
                    
                    return {
                        "status": "success",
                        "data": {
                            "briefing_id": briefing_data.get("briefing_id", "test_briefing"),
                            "date": briefing_data.get("date", datetime.now().isoformat()),
                            "scraped_posts_count": briefing_data.get("scraped_posts_count", 0),
                            "trend_analysis": briefing_data.get("trend_analysis", {
                                "trends": []
                            }),
                            "synthesis_results": briefing_data.get("synthesis_results", {
                                "executive_summary": "No analysis available yet.",
                                "key_insights": [],
                                "actionable_recommendations": [],
                                "market_outlook": "No market outlook available."
                            })
                        }
                    }
        except Exception as e:
            print(f"Error reading test data: {e}")
        
        # Fallback to hardcoded mock data
        return {
            "status": "success",
            "data": {
                "briefing_id": "mock_briefing_001",
                "date": datetime.now().isoformat(),
                "scraped_posts_count": 5,
                "trend_analysis": {
                    "trends": [
                        {
                            "id": "trend_1",
                            "title": "Glass Skin Technique",
                            "description": "Achieving transparent, dewy skin through multi-step routines",
                            "category": "consumer_behavior",
                            "business_impact": "high",
                            "time_to_market": "short_term",
                            "sources": ["social_media", "blogs"],
                            "keywords": ["glass skin", "dewy", "transparent", "routine"]
                        },
                        {
                            "id": "trend_2", 
                            "title": "Cushion Foundation Innovation",
                            "description": "New formulas with skincare benefits and longer wear",
                            "category": "product_type",
                            "business_impact": "medium",
                            "time_to_market": "medium_term",
                            "sources": ["ecommerce", "reviews"],
                            "keywords": ["cushion", "foundation", "skincare", "hyaluronic acid"]
                        },
                        {
                            "id": "trend_3",
                            "title": "Propolis and Honey Extracts",
                            "description": "Natural ingredients with antibacterial and moisturizing properties",
                            "category": "ingredient",
                            "business_impact": "high",
                            "time_to_market": "short_term",
                            "sources": ["research", "formulations"],
                            "keywords": ["propolis", "honey", "natural", "antibacterial"]
                        }
                    ],
                    "priority_trends": [
                        {
                            "id": "priority_1",
                            "title": "Glass Skin Technique",
                            "description": "Achieving transparent, dewy skin through multi-step routines",
                            "reasoning": "High social media engagement and consumer demand",
                            "action_items": ["Develop multi-step routines", "Create educational content"],
                            "business_impact": "high"
                        }
                    ],
                    "market_opportunities": [
                        {
                            "id": "opportunity_1",
                            "title": "Natural Ingredients Market",
                            "description": "Growing demand for clean beauty and natural ingredients",
                            "market_size": "$15 billion by 2025",
                            "entry_barriers": ["Regulatory compliance", "Sourcing challenges"],
                            "competitive_advantage": ["Proven efficacy", "Consumer trust"]
                        }
                    ],
                    "risk_factors": [
                        {
                            "id": "risk_1",
                            "title": "Supply Chain Disruption",
                            "description": "Potential delays in ingredient sourcing from Korea",
                            "severity": "medium",
                            "mitigation_strategies": ["Diversify suppliers", "Local partnerships"]
                        }
                    ],
                    "summary": "K-beauty trends show strong focus on natural ingredients and innovative formulations with high consumer engagement."
                },
                "synthesis_results": {
                    "executive_summary": "K-beauty continues to dominate with glass skin techniques, innovative cushion foundations, and natural ingredients like propolis gaining popularity.",
                    "key_insights": [
                        "Glass skin trend shows no signs of slowing down",
                        "Cushion foundations are evolving with skincare benefits",
                        "Natural ingredients like propolis are becoming mainstream"
                    ],
                    "actionable_recommendations": [
                        "Develop multi-step glass skin routine products",
                        "Create cushion foundations with hyaluronic acid and niacinamide",
                        "Formulate products with propolis and honey extracts"
                    ],
                    "market_outlook": "The K-beauty market is expected to continue growing with focus on natural ingredients and innovative formulations."
                }
            }
        }

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            request_data = json.loads(post_data) if post_data else {}
        except json.JSONDecodeError:
            request_data = {}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if self.path == '/api/trigger':
            # Handle trigger request
            if REAL_DATA_AVAILABLE:
                try:
                    # Initialize the pipeline
                    config = Config()
                    pipeline = Pipeline(config)
                    
                    # Run the analysis (this will take some time)
                    result = pipeline.run_analysis()
                    
                    response = {
                        "status": "success",
                        "message": "Analysis completed successfully",
                        "briefing_id": result.get("briefing_id", "new_briefing"),
                        "timestamp": datetime.now().isoformat()
                    }
                except Exception as e:
                    print(f"Error running analysis: {e}")
                    response = {
                        "status": "error",
                        "message": f"Failed to run analysis: {str(e)}"
                    }
            else:
                response = {
                    "status": "error",
                    "message": "Real analysis not available - using mock data"
                }
        else:
            # For other POST requests, delegate to GET
            response = {"status": "success", "message": "POST request handled"}
        
        self.wfile.write(json.dumps(response).encode())
        return

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return 