from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models, schemas
from app.core import security
from datetime import timedelta

router = APIRouter()

# Dummy accounts for fast local testing
DUMMY_ADMIN = {
    "email": "admin@roadsafety.local",
    "fullname": "System Admin",
    "password": "admin123",
    "is_admin": True,
}

DUMMY_USER = {
    "email": "operator@roadsafety.local",
    "fullname": "Traffic Operator",
    "password": "user123",
    "is_admin": False,
}


def _create_user_if_missing(db: Session, payload: dict):
    existing = db.query(models.User).filter(models.User.email == payload["email"]).first()
    if existing:
        return existing

    new_user = models.User(
        email=payload["email"],
        fullname=payload["fullname"],
        hashed_password=security.get_password_hash(payload["password"]),
        is_admin=payload["is_admin"],
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def ensure_dummy_users(db: Session):
    """Ensure fixed dummy admin/user accounts exist for local testing."""
    _create_user_if_missing(db, DUMMY_ADMIN)
    _create_user_if_missing(db, DUMMY_USER)

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        fullname=user.fullname,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    ensure_dummy_users(db)

    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    requested_role = form_data.scopes[0] if form_data.scopes else None
    if requested_role == "admin" and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    if requested_role == "user" and user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Use admin login for this account")
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email, "role": "admin" if user.is_admin else "user"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/dummy-credentials")
def get_dummy_credentials():
    """Expose local testing credentials for UI helpers."""
    return {
        "admin": {"email": DUMMY_ADMIN["email"], "password": DUMMY_ADMIN["password"]},
        "user": {"email": DUMMY_USER["email"], "password": DUMMY_USER["password"]},
    }

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(security.get_current_user)):
    """Get current user information including role."""
    return current_user

@router.post("/logout")
def logout_user():
    """Logout endpoint (token invalidation handled on client-side or via token blacklist)."""
    return {"message": "Successfully logged out"}
