from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from app.api.v1 import search, filters
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VNU Research API",
    description="API ",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(filters.router, prefix="/api/v1/filters", tags=["filters"])

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "VNU Research API is running (Refactored Architecture)",
        "features": ["PostgreSQL Search", "Filters", "Project Details"]
    }
