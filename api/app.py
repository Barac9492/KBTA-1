#!/usr/bin/env python3
"""
K-Beauty Trend Agent API
FastAPI application for manual agent runs and webhook triggers.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import os

from fastapi import FastAPI, HTTPException, BackgroundTasks, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Import our modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

from scripts.run_agents import TrendAgentRunner
from scripts.push_to_notion import NotionTrendPublisher

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="K-Beauty Trend Agent API",
    description="API for K-beauty trend analysis and synthesis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class TriggerRequest(BaseModel):
    """Request model for triggering trend analysis."""
    force_refresh: bool = False
    include_notion_push: bool = True
    analysis_type: str = "full"  # "full", "trends_only", "synthesis_only"

class WebhookRequest(BaseModel):
    """Request model for webhook triggers."""
    source: str
    event_type: str
    data: Optional[Dict] = None

class TrendResponse(BaseModel):
    """Response model for trend data."""
    status: str
    message: str
    data: Optional[Dict] = None
    timestamp: str

# Global state for tracking analysis runs
analysis_status = {
    "is_running": False,
    "last_run": None,
    "last_status": "idle"
}

def get_output_dir():
    """Get the appropriate output directory based on environment."""
    if os.getenv("VERCEL"):
        return Path("/tmp")
    else:
        return Path("output")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "K-Beauty Trend Agent API",
        "version": "1.0.0",
        "endpoints": {
            "trigger": "POST /trigger - Manually trigger trend analysis",
            "trends": "GET /trends - Get latest trends from cache",
            "latest": "GET /latest - Get latest briefing data",
            "markdown": "GET /markdown - Stream latest briefing as markdown",
            "webhook": "POST /webhook - Webhook endpoint for automated triggers",
            "status": "GET /status - Get current analysis status",
            "health": "GET /health - Health check"
        }
    }

@app.get("/status")
async def get_status():
    """Get current analysis status."""
    return {
        "is_running": analysis_status["is_running"],
        "last_run": analysis_status["last_run"],
        "last_status": analysis_status["last_status"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/latest")
async def get_latest_briefing():
    """Get the latest briefing data."""
    try:
        output_dir = get_output_dir()
        
        # Look for the most recent JSON file
        json_files = list(output_dir.glob("kbeauty_briefing_*.json"))
        
        if not json_files:
            # Try to find any briefing files
            all_files = list(output_dir.glob("*briefing*"))
            if not all_files:
                raise HTTPException(
                    status_code=404,
                    detail="No briefing data available. Please run analysis first."
                )
            
            # If no JSON files, return basic info
            return {
                "status": "no_json_data",
                "message": "Briefing files exist but no JSON data available",
                "available_files": [f.name for f in all_files],
                "timestamp": datetime.now().isoformat()
            }
        
        # Get the most recent file
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "status": "success",
            "message": "Latest briefing data retrieved successfully",
            "data": data,
            "filename": latest_file.name,
            "last_modified": datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat(),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error retrieving latest briefing: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving latest briefing: {str(e)}"
        )

@app.get("/markdown")
async def get_latest_markdown():
    """Stream the latest briefing as markdown."""
    try:
        output_dir = get_output_dir()
        
        # Look for the most recent markdown file
        md_files = list(output_dir.glob("kbeauty_briefing_*.md"))
        
        if not md_files:
            raise HTTPException(
                status_code=404,
                detail="No markdown briefing available. Please run analysis first."
            )
        
        # Get the most recent file
        latest_file = max(md_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Return as streaming response with proper headers
        return Response(
            content=content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f"inline; filename={latest_file.name}",
                "Cache-Control": "no-cache"
            }
        )
        
    except Exception as e:
        logger.error(f"Error retrieving markdown: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving markdown: {str(e)}"
        )

@app.get("/download/json")
async def download_latest_json():
    """Download the latest briefing as JSON file."""
    try:
        output_dir = get_output_dir()
        
        # Look for the most recent JSON file
        json_files = list(output_dir.glob("kbeauty_briefing_*.json"))
        
        if not json_files:
            raise HTTPException(
                status_code=404,
                detail="No JSON briefing available. Please run analysis first."
            )
        
        # Get the most recent file
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return Response(
            content=content,
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename={latest_file.name}",
                "Cache-Control": "no-cache"
            }
        )
        
    except Exception as e:
        logger.error(f"Error downloading JSON: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading JSON: {str(e)}"
        )

@app.post("/trigger", response_model=TrendResponse)
async def trigger_analysis(request: TriggerRequest, background_tasks: BackgroundTasks):
    """Manually trigger trend analysis."""
    global analysis_status
    
    if analysis_status["is_running"]:
        raise HTTPException(
            status_code=409,
            detail="Analysis is already running. Please wait for completion."
        )
    
    # Update status
    analysis_status["is_running"] = True
    analysis_status["last_run"] = datetime.now().isoformat()
    analysis_status["last_status"] = "started"
    
    # Add background task
    background_tasks.add_task(
        run_analysis_pipeline,
        request.force_refresh,
        request.include_notion_push,
        request.analysis_type
    )
    
    return TrendResponse(
        status="started",
        message="Trend analysis pipeline started",
        timestamp=datetime.now().isoformat()
    )

@app.get("/trends", response_model=TrendResponse)
async def get_trends():
    """Get latest trends from cache."""
    try:
        trends_file = Path("data/latest_trends.json")
        
        if not trends_file.exists():
            raise HTTPException(
                status_code=404,
                detail="No trend data available. Please run analysis first."
            )
        
        with open(trends_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return TrendResponse(
            status="success",
            message="Trend data retrieved successfully",
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error retrieving trends: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving trends: {str(e)}"
        )

@app.post("/webhook", response_model=TrendResponse)
async def webhook_trigger(request: WebhookRequest, background_tasks: BackgroundTasks):
    """Webhook endpoint for automated triggers."""
    global analysis_status
    
    # Validate webhook request
    if not request.source or not request.event_type:
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook request: source and event_type are required"
        )
    
    logger.info(f"Webhook received from {request.source}: {request.event_type}")
    
    # Check if analysis is already running
    if analysis_status["is_running"]:
        return TrendResponse(
            status="skipped",
            message="Analysis already running, webhook ignored",
            timestamp=datetime.now().isoformat()
        )
    
    # Update status
    analysis_status["is_running"] = True
    analysis_status["last_run"] = datetime.now().isoformat()
    analysis_status["last_status"] = "webhook_triggered"
    
    # Add background task for webhook-triggered analysis
    background_tasks.add_task(
        run_analysis_pipeline,
        force_refresh=False,
        include_notion_push=True,
        analysis_type="full"
    )
    
    return TrendResponse(
        status="webhook_received",
        message=f"Webhook from {request.source} processed",
        timestamp=datetime.now().isoformat()
    )

async def run_analysis_pipeline(
    force_refresh: bool = False,
    include_notion_push: bool = True,
    analysis_type: str = "full"
):
    """Run the complete analysis pipeline in background."""
    global analysis_status
    
    try:
        logger.info(f"Starting analysis pipeline: {analysis_type}")
        
        # Initialize agent runner
        runner = TrendAgentRunner()
        
        # Run analysis based on type
        if analysis_type in ["full", "trends_only"]:
            await runner.run_full_analysis()
        
        # Push to Notion if requested
        if include_notion_push and analysis_type in ["full", "synthesis_only"]:
            try:
                publisher = NotionTrendPublisher()
                publisher.publish_to_notion()
                logger.info("Successfully pushed to Notion")
            except Exception as e:
                logger.error(f"Error pushing to Notion: {e}")
        
        # Update status
        analysis_status["is_running"] = False
        analysis_status["last_status"] = "completed"
        logger.info("Analysis pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {e}")
        analysis_status["is_running"] = False
        analysis_status["last_status"] = "failed"
        
        # Log error details
        error_details = {
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "analysis_type": analysis_type
        }
        
        # Save error to file
        error_file = get_output_dir() / "analysis_error.json"
        error_file.parent.mkdir(exist_ok=True)
        with open(error_file, 'w') as f:
            json.dump(error_details, f, indent=2)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/config")
async def get_config():
    """Get current configuration (without sensitive data)."""
    return {
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "notion_configured": bool(os.getenv("NOTION_TOKEN") and os.getenv("NOTION_DATABASE_ID")),
        "data_directory": str(Path("data").absolute()),
        "agents_directory": str(Path("agents").absolute()),
        "output_directory": str(get_output_dir()),
        "vercel_environment": bool(os.getenv("VERCEL"))
    }

if __name__ == "__main__":
    import uvicorn
    
    # Run the API server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 