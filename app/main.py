"""
FastAPI application entry point.

Responsibilities:
- App initialization
- Health check
NO business logic here.
"""

from fastapi import FastAPI
from app.config import settings
from app.core.logging import get_logger
from app.api.datasets import router as datasets_router
from app.api.query import router as query_router


logger = get_logger()

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
async def health():
    """
    Health endpoint for monitoring & load balancers.
    """
    logger.info("Health check called")
    return {"status": "ok"}

# Include dataset-related API routes
app.include_router(datasets_router)
app.include_router(query_router)
