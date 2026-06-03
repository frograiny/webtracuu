from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request  # type: ignore
from fastapi.security import OAuth2PasswordBearer  # type: ignore
from pydantic import BaseModel  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from datetime import datetime, timezone
from app.core.exceptions import ConflictError, NotFoundError, ForbiddenError
from app.core.security import create_access_token, create_refresh_token, decode_access_token, decode_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserCreate, UserRead, RefreshRequest
from app.core.rate_limit import limiter

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email.lower()).first()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if not user_id:
        raise credentials_error

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise credentials_error
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure user has Admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def get_current_viewer(current_user: User = Depends(get_current_user)) -> User:
    """Dependency to ensure user has Viewer or Admin role."""
    if current_user.role not in ["viewer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Viewer access required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if get_user_by_email(db, email):
        raise ConflictError("Email đã được đăng ký")

    user_count = db.query(User).count()
    user = User(
        id=str(uuid4()),
        email=email,
        full_name=payload.full_name.strip(),
        hashed_password=get_password_hash(payload.password),
        role="admin" if user_count == 0 else "viewer",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị vô hiệu hóa")

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
        "user": user,
    }

@router.post("/refresh")
async def refresh_token(request: Request, payload: RefreshRequest, db: Session = Depends(get_db)):
    """Cấp lại Access Token mới dựa trên Refresh Token hợp lệ."""
    token_data = decode_token(payload.refresh_token)
    if not token_data or token_data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    jti = token_data.get("jti")
    is_blacklisted = await request.app.state.redis.get(f"blacklist:{jti}")
    if is_blacklisted:
         raise HTTPException(status_code=401, detail="Token has been revoked")

    user_id = token_data.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
        
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(request: Request, payload: RefreshRequest):
    """Đăng xuất và đưa Refresh Token vào danh sách đen (Blacklist)."""
    token_data = decode_token(payload.refresh_token)
    if token_data and token_data.get("type") == "refresh":
        jti = token_data.get("jti")
        exp = token_data.get("exp")
        now = datetime.now(timezone.utc).timestamp()
        ttl = int(exp - now)
        if ttl > 0:
            await request.app.state.redis.setex(f"blacklist:{jti}", ttl, "true")
    return {"status": "success", "message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# ────────────────────────────────────────────────────
# User Management (Admin Only)
# ────────────────────────────────────────────────────


class UpdateUserRoleRequest(BaseModel):
    """Request body for updating user role."""
    role: str  # "admin" or "viewer"


class UpdateUserRoleResponse(BaseModel):
    """Response for updating user role."""
    status: str = "success"
    data: UserRead


@router.get("/users", response_model=dict)
def list_users(
    limit: int = Query(20, ge=1, le=100, description="Số lượng kết quả trả về"),
    offset: int = Query(0, ge=0, description="Bỏ qua bao nhiêu kết quả"),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    List all users with pagination.
    
    Only admin can access this endpoint.
    """
    query = db.query(User)
    total_count = query.count()
    users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "status": "success",
        "data": {
            "total": total_count,
            "items": [
                {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                }
                for user in users
            ]
        }
    }


@router.patch("/users/{user_id}", response_model=UpdateUserRoleResponse)
def update_user_role(
    user_id: str,
    payload: UpdateUserRoleRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Update user role.
    
    Only admin can access this endpoint.
    """
    # Validate role
    if payload.role not in ["admin", "viewer"]:
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'viewer'")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError("Người dùng không tồn tại")
    
    user.role = payload.role
    db.commit()
    db.refresh(user)
    
    return UpdateUserRoleResponse(data=user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Delete a user.
    
    Only admin can access this endpoint.
    """
    # Prevent deleting self
    if user_id == current_admin.id:
        raise ConflictError("Không thể tự xóa tài khoản của chính mình")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError("Người dùng không tồn tại")
    
    db.delete(user)
    db.commit()
    
    return None


@router.patch("/users/{user_id}/deactivate", response_model=UpdateUserRoleResponse)
def deactivate_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    """
    Deactivate a user.
    
    Only admin can access this endpoint.
    """
    # Prevent deactivating self
    if user_id == current_admin.id:
        raise ConflictError("Không thể tự vô hiệu hóa tài khoản của chính mình")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError("Người dùng không tồn tại")
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return UpdateUserRoleResponse(data=user)
