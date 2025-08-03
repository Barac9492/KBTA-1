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
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from core.config import config
from core.pipeline import DailyBriefingPipeline, PipelineScheduler
from core.models import DailyBriefing, PipelineStatus

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

# Global pipeline instance
pipeline = DailyBriefingPipeline()
scheduler = PipelineScheduler()

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

# Dependency injection
def get_pipeline() -> DailyBriefingPipeline:
    """Get pipeline instance."""
    return pipeline

def get_scheduler() -> PipelineScheduler:
    """Get scheduler instance."""
    return scheduler

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

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "config": {
            "openai_configured": bool(config.llm.openai_api_key),
            "notion_configured": config.notion.enabled,
            "output_dir": str(config.output.output_dir)
        }
    }

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current pipeline status."""
    status = pipeline.get_status()
    return StatusResponse(
        status=status.status,
        start_time=status.start_time.isoformat() if status.start_time else None,
        end_time=status.end_time.isoformat() if status.end_time else None,
        error_message=status.error_message,
        briefing_id=status.briefing_id
    )

@app.post("/trigger", response_model=BriefingResponse)
async def trigger_briefing(
    request: TriggerRequest,
    background_tasks: BackgroundTasks,
    pipeline: DailyBriefingPipeline = Depends(get_pipeline)
):
    """Manually trigger a daily briefing."""
    current_status = pipeline.get_status()
    
    if current_status.status == "running":
        raise HTTPException(
            status_code=409,
            detail="Pipeline is already running. Please wait for completion."
        )
    
    # Add background task
    background_tasks.add_task(
        run_briefing_pipeline,
        pipeline,
        request.force_run,
        request.include_notion,
        request.include_markdown,
        request.include_json
    )
    
    return BriefingResponse(
        status="started",
        message="Daily briefing pipeline started",
        timestamp=datetime.now().isoformat()
    )

@app.get("/trigger", response_model=BriefingResponse)
async def trigger_briefing_simple():
    """Simple GET endpoint to trigger a briefing."""
    try:
        # Check if pipeline is already running
        current_status = pipeline.get_status()
        if current_status.status == "running":
            return BriefingResponse(
                status="running",
                message="Pipeline is already running. Please wait for completion.",
                timestamp=datetime.now().isoformat()
            )
        
        # Start the briefing pipeline
        briefing = await run_briefing_pipeline(
            pipeline,
            force_run=False,
            include_notion=False,  # Disable Notion for simplicity
            include_markdown=True,
            include_json=True
        )
        
        if briefing:
            return BriefingResponse(
                status="success",
                message="Briefing generated successfully",
                briefing_id=briefing.briefing_id,
                timestamp=datetime.now().isoformat(),
                data=briefing.to_dict()
            )
        else:
            return BriefingResponse(
                status="failed",
                message="Failed to generate briefing",
                timestamp=datetime.now().isoformat()
            )
            
    except Exception as e:
        logger.error(f"Error triggering briefing: {e}")
        return BriefingResponse(
            status="error",
            message=f"Error generating briefing: {str(e)}",
            timestamp=datetime.now().isoformat()
        )

@app.get("/latest", response_model=BriefingResponse)
async def get_latest_briefing():
    """Get the latest briefing data."""
    try:
        briefing_data = pipeline.get_latest_briefing()
        
        if not briefing_data:
            # Return a helpful message instead of 404 error
            return BriefingResponse(
                status="no_data",
                message="No briefing data available yet. Please trigger a briefing first using POST /trigger",
                timestamp=datetime.now().isoformat(),
                data={
                    "message": "No briefing has been generated yet. Use the trigger endpoint to create your first briefing.",
                    "suggestion": "POST /trigger to generate a new briefing"
                }
            )
        
        return BriefingResponse(
            status="success",
            message="Latest briefing retrieved successfully",
            briefing_id=briefing_data.get("briefing_id"),
            timestamp=datetime.now().isoformat(),
            data=briefing_data
        )
        
    except Exception as e:
        logger.error(f"Error retrieving latest briefing: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving briefing: {str(e)}"
        )

@app.get("/download/{format}")
async def download_briefing(format: str):
    """Download briefing files in specified format."""
    try:
        output_dir = config.output.output_dir
        
        if format == "markdown":
            files = list(output_dir.glob("kbeauty_briefing_*.md"))
        elif format == "json":
            files = list(output_dir.glob("kbeauty_briefing_*.json"))
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid format. Use 'markdown' or 'json'"
            )
        
        if not files:
            raise HTTPException(
                status_code=404,
                detail=f"No {format} files available"
            )
        
        # Get the most recent file
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        
        return FileResponse(
            path=latest_file,
            filename=latest_file.name,
            media_type="text/plain" if format == "markdown" else "application/json"
        )
        
    except Exception as e:
        logger.error(f"Error downloading briefing: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading briefing: {str(e)}"
        )

@app.post("/webhook", response_model=BriefingResponse)
async def webhook_trigger(
    request: WebhookRequest,
    background_tasks: BackgroundTasks,
    pipeline: DailyBriefingPipeline = Depends(get_pipeline)
):
    """Webhook endpoint for automated triggers."""
    # Validate webhook request
    if not request.source or not request.event_type:
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook request: source and event_type are required"
        )
    
    logger.info(f"Webhook received from {request.source}: {request.event_type}")
    
    # Check if pipeline is already running
    current_status = pipeline.get_status()
    if current_status.status == "running":
        return BriefingResponse(
            status="skipped",
            message="Pipeline already running, webhook ignored",
            timestamp=datetime.now().isoformat()
        )
    
    # Add background task for webhook-triggered briefing
    background_tasks.add_task(
        run_briefing_pipeline,
        pipeline,
        force_run=False,
        include_notion=True,
        include_markdown=True,
        include_json=True
    )
    
    return BriefingResponse(
        status="webhook_received",
        message=f"Webhook from {request.source} processed",
        timestamp=datetime.now().isoformat()
    )

@app.post("/scheduler/start")
async def start_scheduler(scheduler: PipelineScheduler = Depends(get_scheduler)):
    """Start the automated scheduler."""
    try:
        # Start scheduler in background
        asyncio.create_task(scheduler.start_scheduler())
        
        return {
            "status": "started",
            "message": "Automated scheduler started",
            "schedule_time": config.pipeline.schedule_time,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error starting scheduler: {str(e)}"
        )

@app.post("/scheduler/stop")
async def stop_scheduler(scheduler: PipelineScheduler = Depends(get_scheduler)):
    """Stop the automated scheduler."""
    try:
        scheduler.stop_scheduler()
        
        return {
            "status": "stopped",
            "message": "Automated scheduler stopped",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error stopping scheduler: {str(e)}"
        )

async def run_briefing_pipeline(
    pipeline: DailyBriefingPipeline,
    force_run: bool = False,
    include_notion: bool = True,
    include_markdown: bool = True,
    include_json: bool = True
):
    """Run the briefing pipeline in background."""
    try:
        logger.info("Starting briefing pipeline...")
        
        # Temporarily override output settings
        original_notion = config.output.notion_enabled
        original_markdown = config.output.markdown_enabled
        original_json = config.output.json_enabled
        
        config.output.notion_enabled = include_notion
        config.output.markdown_enabled = include_markdown
        config.output.json_enabled = include_json
        
        # Run the pipeline
        briefing = await pipeline.run_daily_briefing()
        
        # Restore original settings
        config.output.notion_enabled = original_notion
        config.output.markdown_enabled = original_markdown
        config.output.json_enabled = original_json
        
        if briefing:
            logger.info(f"Briefing completed: {briefing.briefing_id}")
        else:
            logger.error("Briefing failed")
            
    except Exception as e:
        logger.error(f"Error in briefing pipeline: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=config.api_host if hasattr(config, 'api_host') else "0.0.0.0",
        port=config.api_port if hasattr(config, 'api_port') else 8000,
        reload=True,
        log_level="info"
    ) 