from fastapi import FastAPI 
from app.config import settings
from app.api.routes import documents

#create FastAPI app instance
app=FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="DocuMind AI - Multi-Agent Document Intelligence System"
)

# Include routers
app.include_router(documents.router)

#health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running

    """
    return {
        "status":"Healthy",
        "app_name":settings.app_name,
        "version":"1.0.0"
    }

@app.get("/")
async def root():
    """
    Root endpoint-API information

    """
    return {
        "message":"Welcome to DocuMind AI API",
        "version":"1.0.0",
        "docs":"/docs",
        "health":"/health"
    }