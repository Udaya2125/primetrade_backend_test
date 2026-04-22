from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserPublic, UserUpdate


def serialize_user(document: dict | None) -> UserPublic | None:
    if document is None:
        return None
    return UserPublic(
        id=str(document["_id"]),
        email=document["email"],
        full_name=document.get("full_name"),
        role=document.get("role", "user"),
        is_active=document.get("is_active", True),
        created_at=document.get("created_at"),
    )


async def get_user_by_email(database, email: str) -> UserPublic | None:
    document = await database.users.find_one({"email": email.lower()})
    return serialize_user(document)


async def get_user_by_id(database, user_id: str) -> UserPublic | None:
    try:
        document = await database.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None
    return serialize_user(document)


async def create_user(database, user_in: UserCreate) -> UserPublic:
    existing_user = await database.users.find_one({"email": user_in.email.lower()})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

    now = datetime.now(timezone.utc)
    result = await database.users.insert_one(
        {
            "email": user_in.email.lower(),
            "full_name": user_in.full_name,
            "hashed_password": get_password_hash(user_in.password),
            "role": "user",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
    )
    created_user = await database.users.find_one({"_id": result.inserted_id})
    user = serialize_user(created_user)
    if user is None:
        raise RuntimeError("User creation failed")
    return user


async def authenticate_user(database, email: str, password: str) -> UserPublic | None:
    document = await database.users.find_one({"email": email.lower()})
    if not document:
        return None
    if not verify_password(password, document["hashed_password"]):
        return None
    return serialize_user(document)


async def update_current_user(database, user_id: str, user_update: UserUpdate) -> UserPublic | None:
    update_data = {key: value for key, value in user_update.model_dump(exclude_unset=True).items() if value is not None}
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    if not update_data:
        return await get_user_by_id(database, user_id)

    update_data["updated_at"] = datetime.now(timezone.utc)
    await database.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    return await get_user_by_id(database, user_id)
