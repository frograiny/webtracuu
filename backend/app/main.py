from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.exceptions import RequestValidationError  # type: ignore
from fastapi.responses import JSONResponse, RedirectResponse  # type: ignore
from app.api.v1 import auth, filters, search
from app.core.config import settings
from app.core.exceptions import APIException
import asyncio
import sys
from loguru import logger
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

# Cấu hình Loguru
logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
logger.add("logs/app_{time:YYYY-MM-DD}.log", rotation="10 MB", retention="10 days", level="INFO")


class LocalRedisFallback:
    def __init__(self):
        self._store = {}

    async def get(self, key: str):
        item = self._store.get(key)
        if not item:
            return None
        value, expires_at = item
        if expires_at and expires_at <= asyncio.get_running_loop().time():
            self._store.pop(key, None)
            return None
        return value

    async def setex(self, key: str, ttl: int, value: str):
        self._store[key] = (value, asyncio.get_running_loop().time() + ttl)


def setup_admin_user(db):
    """Helper to pre-provision the default system admin account."""
    from app.models.user import User
    from app.core.security import get_password_hash, verify_password
    from uuid import uuid4

    admin_email = settings.ADMIN_EMAIL.lower()
    admin_user = db.query(User).filter(User.email == admin_email).first()
    if not admin_user:
        logger.info(f"Admin user {admin_email} not found. Creating...")
        admin_user = User(
            id=str(uuid4()),
            email=admin_email,
            full_name="System Administrator",
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        logger.info("Admin user created successfully.")
    else:
        updated = False
        if not verify_password(settings.ADMIN_PASSWORD, admin_user.hashed_password):
            logger.info("Admin password has changed. Updating password hash...")
            admin_user.hashed_password = get_password_hash(settings.ADMIN_PASSWORD)
            updated = True
        if admin_user.role != "admin":
            logger.info("Updating admin user role to admin...")
            admin_user.role = "admin"
            updated = True
        if not admin_user.is_active:
            logger.info("Activating admin user...")
            admin_user.is_active = True
            updated = True
            
        if updated:
            db.commit()
            db.refresh(admin_user)
            logger.info("Admin user configuration synchronized successfully.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = None
    try:
        logger.info("Initializing cache with Redis...")
        redis = aioredis.from_url(
            settings.REDIS_URL,
            socket_connect_timeout=0.2,
            socket_timeout=0.2,
        )
        await redis.ping()
        app.state.redis = redis
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    except Exception as exc:
        logger.warning(f"Redis unavailable, using in-memory cache: {exc}")
        app.state.redis = LocalRedisFallback()
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

    try:
        from app.db.session import SessionLocal
        logger.info("Pre-provisioning admin user...")
        db = SessionLocal()
        try:
            setup_admin_user(db)
        finally:
            db.close()
    except Exception as exc:
        logger.warning(f"Database unavailable for admin pre-provisioning: {exc}")

    yield
    logger.info("Shutting down...")
    if redis is not None:
        await redis.aclose()

app = FastAPI(
    title="VNU Research API",
    description="API with Rate Limiting, Caching and Observability",
    version="1.0.0",
    lifespan=lifespan,
)

# Đăng ký Prometheus Metrics
Instrumentator().instrument(app).expose(app)

# Đăng ký Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(search.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(filters.router, prefix="/api/v1/filters", tags=["filters"])


@app.get("/", include_in_schema=False)
def root():
    """Redirect root path to API docs."""
    return RedirectResponse(url="/docs")


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

@app.get("/health", tags=["ops"])
async def health_check():
    """Endpoint for ops basics: container health check."""
    return {"status": "ok", "service": "vnu_research_backend"}


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
