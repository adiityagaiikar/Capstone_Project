from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import models
import schemas
import security
from datetime import timedelta

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate):
    # Check for duplicate email
    existing = await models.User.find_one(models.User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = security.get_password_hash(user.password)
    new_user = models.User(
        fullname=user.fullname,
        email=user.email,
        hashed_password=hashed_pw,
    )
    await new_user.insert()

    return _user_to_response(new_user)


@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await models.User.find_one(models.User.email == form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = security.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
async def read_me(current_user: models.User = Depends(security.get_current_user)):
    return _user_to_response(current_user)


# ── Helper ────────────────────────────────────────────────────────────────────

def _user_to_response(user: models.User) -> schemas.UserResponse:
    """Convert a Beanie User document to the API response schema."""
    return schemas.UserResponse(
        id=str(user.id),
        fullname=user.fullname,
        email=user.email,
        is_admin=user.is_admin,
        is_active=user.is_active,
        subscription_plan=user.subscription_plan,
        razorpay_customer_id=user.razorpay_customer_id,
    )
