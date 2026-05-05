from slowapi import Limiter
from fastapi import Request

def get_rate_limit_key(request: Request) -> str:
    """
    Tạo khóa (key) cho Rate Limiter.
    Nếu User đã đăng nhập (có token) -> dùng Token làm key.
    Nếu là Guest -> dùng IP + User-Agent để tránh block nhầm mạng NAT.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return f"token:{token}"
    
    ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("User-Agent", "unknown")
    return f"guest:{ip}_{ua}"

limiter = Limiter(key_func=get_rate_limit_key)
