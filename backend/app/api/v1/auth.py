from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status  # type: ignore
from fastapi.security import OAuth2PasswordBearer  # type: ignore
from pydantic import BaseModel  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.core.exceptions import ConflictError, NotFoundError, ForbiddenError
from app.core.security import create_access_token, decode_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserCreate, UserRead

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
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Tài khoản đã bị vô hiệu hóa")

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
        "user": user,
    }


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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all users.
    
    Only admin can access this endpoint.
    """
    if current_user.role != "admin":
        raise ForbiddenError("Chỉ admin có thể xem danh sách người dùng")
    
    users = db.query(User).all()
    return {
        "status": "success",
        "data": [
            {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            for user in users
        ],
    }


@router.patch("/users/{user_id}", response_model=UpdateUserRoleResponse)
def update_user_role(
    user_id: str,
    payload: UpdateUserRoleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update user role.
    
    Only admin can access this endpoint.
    """
    if current_user.role != "admin":
        raise ForbiddenError("Chỉ admin có thể cập nhật vai trò người dùng")
    
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
    current_user: User = Depends(get_current_user),
):
    """
    Delete a user.
    
    Only admin can access this endpoint.
    """
    if current_user.role != "admin":
        raise ForbiddenError("Chỉ admin có thể xóa người dùng")
    
    # Prevent deleting self
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Không thể xóa chính mình")
    
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
    current_user: User = Depends(get_current_user),
):
    """
    Deactivate a user.
    
    Only admin can access this endpoint.
    """
    if current_user.role != "admin":
        raise ForbiddenError("Chỉ admin có thể vô hiệu hóa người dùng")
    
    # Prevent deactivating self
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Không thể vô hiệu hóa chính mình")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundError("Người dùng không tồn tại")
    
    user.is_active = False
    db.commit()
    db.refresh(user)
    
    return UpdateUserRoleResponse(data=user)
