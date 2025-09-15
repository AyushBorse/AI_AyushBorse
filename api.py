from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Dict, Any
import uuid
import os

from .models import VideoRequest, VideoResponse
from cognimate.core.pipeline_orchestrator import PipelineOrchestrator
from cognimate.utils.config_loader import load_config

app = FastAPI(
    title="CogniMate API",
    description="API for AI-powered educational video generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration
config = load_config()

# Initialize pipeline orchestrator
pipeline = PipelineOrchestrator(config)

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest) -> VideoResponse:
    """
    Generate an educational video based on a concept query.
    
    Args:
        request: VideoRequest containing query and sector information
        
    Returns:
        VideoResponse with video information and metadata
    """
    try:
        result = pipeline.process_query(request.query, request.sector)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return VideoResponse(
            video_id=str(uuid.uuid4()),
            query=result["query"],
            sector=result["sector"],
            video_path=result["video_path"],
            metadata=result["metadata"],
            status="completed"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/video/{video_id}")
async def get_video(video_id: str):
    """
    Retrieve a generated video by ID.
    
    Args:
        video_id: The ID of the video to retrieve
        
    Returns:
        The video file
    """
    # In a real implementation, you would look up the video path from a database
    video_path = f"output/{video_id}.mp4"
    
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")
        
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{video_id}.mp4"
    )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}