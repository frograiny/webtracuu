"""Custom exception classes for the VNU Research API."""

from fastapi import HTTPException, status


class APIException(HTTPException):
    """Base exception class for API errors."""
    
    def __init__(self, status_code: int, detail: str, code: str = None):
        self.code = code or "INTERNAL_ERROR"
        super().__init__(status_code=status_code, detail=detail)


class ValidationError(APIException):
    """Raised when input validation fails."""
    
    def __init__(self, detail: str, code: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            code=code,
        )


class NotFoundError(APIException):
    """Raised when a resource is not found."""
    
    def __init__(self, detail: str = "Resource not found", code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code=code,
        )


class UnauthorizedError(APIException):
    """Raised when authentication fails."""
    
    def __init__(self, detail: str = "Authentication failed", code: str = "UNAUTHORIZED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code=code,
        )


class ForbiddenError(APIException):
    """Raised when user lacks required permissions."""
    
    def __init__(self, detail: str = "Access denied", code: str = "FORBIDDEN"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code=code,
        )


class ConflictError(APIException):
    """Raised when a resource already exists (duplicate)."""
    
    def __init__(self, detail: str = "Resource already exists", code: str = "CONFLICT"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            code=code,
        )


class InternalServerError(APIException):
    """Raised for internal server errors."""
    
    def __init__(self, detail: str = "Internal server error", code: str = "INTERNAL_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            code=code,
        )
