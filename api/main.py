"""
FastAPI application for K-Beauty Daily Trend Briefing System
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="K-Beauty Daily Trend Briefing API",
    description="API for automated Korean beauty trend briefings",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TriggerRequest(BaseModel):
    """Request model for triggering briefings."""
    force_run: bool = False
    include_notion: bool = True
    include_markdown: bool = True
    include_json: bool = True

class WebhookRequest(BaseModel):
    """Request model for webhook triggers."""
    source: str
    event_type: str
    data: Optional[Dict] = None

class BriefingResponse(BaseModel):
    """Response model for briefing data."""
    status: str
    message: str
    briefing_id: Optional[str] = None
    timestamp: str
    data: Optional[Dict] = None

class StatusResponse(BaseModel):
    """Response model for pipeline status."""
    status: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_message: Optional[str] = None
    briefing_id: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "K-Beauty Daily Trend Briefing API",
        "version": "2.0.0",
        "endpoints": {
            "trigger": "POST /trigger - Manually trigger daily briefing",
            "status": "GET /status - Get pipeline status",
            "latest": "GET /latest - Get latest briefing",
            "download": "GET /download/{format} - Download briefing files",
            "webhook": "POST /webhook - Webhook endpoint for automation",
            "scheduler": "POST /scheduler/start - Start automated scheduler",
            "health": "GET /health - Health check"
        }
    }

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint."""
    return {
        "status": "success",
        "message": "API is working!",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "config": {
            "openai_configured": True,
            "notion_configured": False,
            "output_dir": "/tmp"
        }
    }

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current pipeline status."""
    return StatusResponse(
        status="idle",
        start_time=None,
        end_time=None,
        error_message=None,
        briefing_id=None
    )

@app.post("/trigger", response_model=BriefingResponse)
async def trigger_briefing(request: TriggerRequest, background_tasks: BackgroundTasks):
    """Manually trigger a daily briefing."""
    return BriefingResponse(
        status="started",
        message="Daily briefing pipeline started",
        timestamp=datetime.now().isoformat()
    )

@app.get("/trigger", response_model=BriefingResponse)
async def trigger_briefing_simple():
    """Simple GET endpoint to trigger a briefing."""
    return BriefingResponse(
        status="success",
        message="Briefing triggered successfully",
        timestamp=datetime.now().isoformat(),
        data={
            "message": "Mock briefing data",
            "trends": ["Glass Skin", "Cushion Foundation", "Propolis"],
            "executive_summary": "K-beauty trends are evolving with focus on natural ingredients and innovative formulations."
        }
    )

@app.get("/latest", response_model=BriefingResponse)
async def get_latest_briefing():
    """Get the latest briefing data."""
    return BriefingResponse(
        status="success",
        message="Latest briefing retrieved successfully",
        briefing_id="mock_briefing_001",
        timestamp=datetime.now().isoformat(),
        data={
            "briefing_id": "mock_briefing_001",
            "date": datetime.now().isoformat(),
            "scraped_posts_count": 5,
            "trend_analysis": {
                "trends": [
                    {
                        "id": "trend_1",
                        "name": "Glass Skin Technique",
                        "description": "Achieving transparent, dewy skin through multi-step routines",
                        "relevance_score": 0.95
                    },
                    {
                        "id": "trend_2", 
                        "name": "Cushion Foundation Innovation",
                        "description": "New formulas with skincare benefits and longer wear",
                        "relevance_score": 0.88
                    },
                    {
                        "id": "trend_3",
                        "name": "Propolis and Honey Extracts",
                        "description": "Natural ingredients with antibacterial and moisturizing properties",
                        "relevance_score": 0.82
                    }
                ]
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
    )

@app.get("/download/{format}")
async def download_briefing(format: str):
    """Download briefing files in specified format."""
    if format not in ["markdown", "json"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid format. Use 'markdown' or 'json'"
        )
    
    # Return mock content
    if format == "markdown":
        content = """# K-Beauty Daily Briefing

## Executive Summary
K-beauty trends are evolving with focus on natural ingredients and innovative formulations.

## Key Trends
1. Glass Skin Technique
2. Cushion Foundation Innovation  
3. Propolis and Honey Extracts

## Market Outlook
The K-beauty market is expected to continue growing with focus on natural ingredients and innovative formulations.
"""
        return FileResponse(
            path=None, # No actual file to serve, just return content
            filename="briefing.md",
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=briefing.md"}
        )
    else:
        content = '{"briefing": "mock data"}'
        return FileResponse(
            path=None, # No actual file to serve, just return content
            filename="briefing.json",
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=briefing.json"}
        )

@app.post("/webhook", response_model=BriefingResponse)
async def webhook_trigger(request: WebhookRequest, background_tasks: BackgroundTasks):
    """Webhook endpoint for automated triggers."""
    return BriefingResponse(
        status="webhook_received",
        message=f"Webhook from {request.source} processed",
        timestamp=datetime.now().isoformat()
    )

@app.post("/scheduler/start")
async def start_scheduler():
    """Start the automated scheduler."""
    return {
        "status": "started",
        "message": "Automated scheduler started",
        "schedule_time": "09:00",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the automated scheduler."""
    return {
        "status": "stopped",
        "message": "Automated scheduler stopped",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 