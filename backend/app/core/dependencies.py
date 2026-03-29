"""
Authentication and authorization dependencies.
These functions are commonly used across routers using FastAPI's Depends() system.
"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import security, database
from app.models import models


def get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Dependency to get the current authenticated user.
    Validates the JWT token and returns the user from the database.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    return security.get_current_user(token, db)


def require_admin(current_user: models.User = Depends(get_current_user)):
    """
    Dependency to require admin role.
    Use this on admin-only endpoints to ensure only admins can access.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Admin user
        
    Raises:
        HTTPException(403): If user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required for this operation"
        )
    return current_user
