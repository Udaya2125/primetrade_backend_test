from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.security import decode_token
from app.controllers.user import get_user_by_id
from app.db.database import get_database
from app.schemas.token import TokenData
from app.schemas.user import UserPublic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), database=Depends(get_database)) -> UserPublic:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        token_data = TokenData(subject=payload.get("sub"), role=payload.get("role"))
    except JWTError:
        raise credentials_exception

    if token_data.subject is None:
        raise credentials_exception

    user = await get_user_by_id(database, token_data.subject)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


async def require_admin(current_user: UserPublic = Depends(get_current_user)) -> UserPublic:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user
