from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.controllers.user import get_user_by_id, serialize_user, update_current_user
from app.dependencies.auth import get_current_user, require_admin
from app.db.database import get_database
from app.schemas.user import UserPublic, UserUpdate


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
async def read_me(current_user: UserPublic = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserPublic)
async def update_me(user_update: UserUpdate, current_user: UserPublic = Depends(get_current_user), database=Depends(get_database)):
    updated_user = await update_current_user(database, current_user.id, user_update)
    return updated_user or current_user


@router.get("", response_model=list[UserPublic])
async def read_users(_: UserPublic = Depends(require_admin), database=Depends(get_database)):
    users: list[UserPublic] = []
    async for document in database.users.find({}).sort("created_at", -1):
        serialized = serialize_user(document)
        if serialized is not None:
            users.append(serialized)
    return users


@router.get("/{user_id}", response_model=UserPublic)
async def read_user(user_id: str, _: UserPublic = Depends(require_admin), database=Depends(get_database)):
    user = await get_user_by_id(database, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
