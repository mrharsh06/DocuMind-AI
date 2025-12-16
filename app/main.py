import time
import logging
from fastapi import FastAPI,Request
from app.config import settings
from app.api.routes import documents
from app.api.routes import query
from app.api.routes import admin
from app.core.logging_config import setup_logging


setup_logging()

request_logger=logging.getLogger("app.middleware.request_logger")


#create FastAPI app instance
app=FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="DocuMind AI - Multi-Agent Document Intelligence System"
)


@app.middleware("http")
async def log_requests(request: Request,call_next):
    """
    Simple middleware to log each HTTP request and response.
    Logs method, path, status code, and processing time.
    """
    start_time=time.time()

    response=await call_next(request)

    process_time=(time.time()-start_time)*1000

    log_message=f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms"

    if process_time >500:
        request_logger.warning(log_message)
    else:
        request_logger.info(log_message)
    return response
    
# Include routers
app.include_router(documents.router)
app.include_router(query.router)
app.include_router(admin.router)


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