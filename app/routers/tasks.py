from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, deps, models

router = APIRouter(
    prefix="/tasks", tags=["tasks"], responses={404: {"description": "Not Found"}}
)


@router.post(
    "", response_model=schemas.TaskOut, status_code=201, summary="Create a new task"
)
async def create_task(
    payload: schemas.TaskCreate,
    user=Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
):
    task = models.Task(**payload.model_dump(), owner_id=user.id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.put(
    "/{task_id}",
    response_model=schemas.TaskOut,
    summary="Get a single task by its ID"
)
async def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    user=Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
):
    task: models.Task | None = await db.get(models.Task, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(404, "Task not found")

    data = payload.model_dump(exclude_unset=True)
    if "status" in data:
        data["status"] = models.TaskStatus(data["status"].value)

    for k, v in data.items():
        setattr(task, k, v)
    await db.commit()
    await db.refresh(task)
    return task


@router.get(
    "",
    response_model=list[schemas.TaskOut],
    summary="List all tasks for the current user",
)
async def list_tasks(
    status: schemas.TaskStatus | None = None,
    priority: int | None = None,
    created_from: str | None = Query(None, alias="created_at"),
    db: AsyncSession = Depends(deps.get_db),
    user=Depends(deps.get_current_user),
):
    stmt = select(models.Task).where(models.Task.owner_id == user.id)
    if status:
        stmt = stmt.where(models.Task.status == status)
    if priority is not None:
        stmt = stmt.where(models.Task.priority == priority)
    if created_from:
        stmt = stmt.where(models.Task.created_at >= created_from)
    rows = await db.scalars(stmt.order_by(models.Task.created_at.desc()))
    return rows.all()


@router.get("/search", response_model=list[schemas.TaskOut])
async def search(
    q: str, db: AsyncSession = Depends(deps.get_db), user=Depends(deps.get_current_user)
):
    stmt = select(models.Task).where(
        models.Task.owner_id == user.id,
        or_(models.Task.title.ilike(f"%{q}%"), models.Task.description.ilike(f"%{q}%")),
    )
    rows = await db.scalars(stmt)
    return rows.all()
