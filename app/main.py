"""
FastAPI Application - Biznesplan Generator

Main application file with FastAPI configuration and routes.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Biznesplan Generator",
    description="AI-powered business plan generation system",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS middleware (if needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",
        "service": "biznesplan-generator",
        "version": "0.1.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - will serve dashboard HTML"""
    return {
        "message": "Biznesplan Generator API",
        "docs": "/docs",
        "health": "/health"
    }

# Import and include routers (will be created later)
# from app.routes import orders, dashboard
# app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
# app.include_router(dashboard.router, tags=["dashboard"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
