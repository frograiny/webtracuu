from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.exceptions import RequestValidationError  # type: ignore
from fastapi.responses import JSONResponse  # type: ignore
from app.api.v1 import auth, filters, search
from app.core.config import settings
from app.core.exceptions import APIException
import sys
from loguru import logger
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

# Cấu hình Loguru
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="10 MB", retention="10 days", level="INFO")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Cache (InMemoryBackend)...")
    FastAPICache.init(InMemoryBackend())
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="VNU Research API",
    description="API with Rate Limiting and Caching",
    version="1.0.0",
    lifespan=lifespan,
)

# Đăng ký Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
