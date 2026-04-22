from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.task import create_task, delete_task, list_tasks, update_task
from app.dependencies.auth import get_current_user
from app.db.database import get_database
from app.schemas.task import TaskCreate, TaskPublic, TaskUpdate
from app.schemas.user import UserPublic


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskPublic])
async def read_tasks(current_user: UserPublic = Depends(get_current_user), database=Depends(get_database)):
    return await list_tasks(database, current_user)


@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
async def create_new_task(task_in: TaskCreate, current_user: UserPublic = Depends(get_current_user), database=Depends(get_database)):
    return await create_task(database, current_user.id, task_in)


@router.patch("/{task_id}", response_model=TaskPublic)
async def modify_task(task_id: str, task_update: TaskUpdate, current_user: UserPublic = Depends(get_current_user), database=Depends(get_database)):
    task = await update_task(database, task_id, current_user, task_update)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_task(task_id: str, current_user: UserPublic = Depends(get_current_user), database=Depends(get_database)):
    deleted = await delete_task(database, task_id, current_user)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
