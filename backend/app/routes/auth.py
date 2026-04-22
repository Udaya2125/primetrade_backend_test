from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers.user import authenticate_user, create_user
from app.core.config import get_settings
from app.core.security import create_access_token
from app.db.database import get_database
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserPublic


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, database=Depends(get_database)):
    return await create_user(database, user_in)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), database=Depends(get_database)):
    user = await authenticate_user(database, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    settings = get_settings()
    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        extra_claims={"role": user.role},
    )
    return Token(access_token=access_token)
