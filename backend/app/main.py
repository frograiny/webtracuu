from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.exceptions import RequestValidationError  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from app.api.v1 import auth, filters, search
from app.core.config import settings
from app.core.exceptions import APIException
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
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(search.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(filters.router, prefix="/api/v1/filters", tags=["filters"])


# ────────────────────────────────────────────────────
# Exception Handlers
# ────────────────────────────────────────────────────


@app.exception_handler(APIException)
async def api_exception_handler(request, exc: APIException):
    """Handle custom API exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.code,
            "detail": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"][1:]),
            "message": error["msg"],
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": "VALIDATION_ERROR",
            "detail": "Validation failed",
            "errors": errors,
        },
    )


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "VNU Research API is running (Refactored Architecture)",
        "features": ["PostgreSQL Search", "Filters", "Project Details", "JWT Auth", "CRUD Operations"]
    }
