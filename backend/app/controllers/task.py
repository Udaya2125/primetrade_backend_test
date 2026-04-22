from datetime import datetime, timezone

from bson import ObjectId

from app.schemas.task import TaskCreate, TaskPublic, TaskUpdate
from app.schemas.user import UserPublic


def serialize_task(document: dict | None) -> TaskPublic | None:
    if document is None:
        return None
    return TaskPublic(
        id=str(document["_id"]),
        title=document["title"],
        description=document.get("description"),
        completed=document.get("completed", False),
        owner_id=str(document["owner_id"]),
        created_at=document.get("created_at"),
        updated_at=document.get("updated_at"),
    )


def _task_filter(task_id: str | None, current_user: UserPublic, owner_id: str | None = None) -> dict:
    query: dict = {}
    if task_id is not None:
        query["_id"] = ObjectId(task_id)
    if current_user.role != "admin":
        query["owner_id"] = current_user.id if owner_id is None else owner_id
    elif owner_id is not None:
        query["owner_id"] = owner_id
    return query


async def list_tasks(database, current_user: UserPublic) -> list[TaskPublic]:
    query = {} if current_user.role == "admin" else {"owner_id": current_user.id}
    documents = database.tasks.find(query).sort("created_at", -1)
    tasks = []
    async for document in documents:
        task = serialize_task(document)
        if task is not None:
            tasks.append(task)
    return tasks


async def create_task(database, owner_id: str, task_in: TaskCreate) -> TaskPublic:
    now = datetime.now(timezone.utc)
    result = await database.tasks.insert_one(
        {
            "title": task_in.title,
            "description": task_in.description,
            "completed": False,
            "owner_id": owner_id,
            "created_at": now,
            "updated_at": now,
        }
    )
    document = await database.tasks.find_one({"_id": result.inserted_id})
    task = serialize_task(document)
    if task is None:
        raise RuntimeError("Task creation failed")
    return task


async def get_task_by_id(database, task_id: str, current_user: UserPublic) -> TaskPublic | None:
    try:
        document = await database.tasks.find_one(_task_filter(task_id, current_user))
    except Exception:
        return None
    return serialize_task(document)


async def update_task(database, task_id: str, current_user: UserPublic, task_update: TaskUpdate) -> TaskPublic | None:
    update_data = {key: value for key, value in task_update.model_dump(exclude_unset=True).items() if value is not None}
    if not update_data:
        return await get_task_by_id(database, task_id, current_user)

    update_data["updated_at"] = datetime.now(timezone.utc)
    await database.tasks.update_one(_task_filter(task_id, current_user), {"$set": update_data})
    return await get_task_by_id(database, task_id, current_user)


async def delete_task(database, task_id: str, current_user: UserPublic) -> bool:
    result = await database.tasks.delete_one(_task_filter(task_id, current_user))
    return result.deleted_count == 1
