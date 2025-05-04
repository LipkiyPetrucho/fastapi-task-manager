from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, deps, models
from app.core.security import hash_password, verify_password, create_access, create_refresh

router = APIRouter(prefix="",
                   tags=["auth"],
                   responses={401: {"description": "Unauthorized"}}
                   )


@router.post("/register", response_model=schemas.UserOut, status_code=201, summary="Register a new user")
async def register(payload: schemas.UserCreate, db: AsyncSession = Depends(deps.get_db)):
    exists = await db.scalar(select(models.User).where(models.User.email == payload.email))
    if exists:
        raise HTTPException(400, "Email already registered")
    user = models.User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token, summary="Authenticate user and return JWT tokens")
async def login(form: schemas.UserCreate, db: AsyncSession = Depends(deps.get_db)):
    user = await db.scalar(select(models.User).where(models.User.email == form.email))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials")
    return {"access": create_access(str(user.id)), "refresh": create_refresh(str(user.id))}


@router.post("/refresh", response_model=schemas.Token, summary="Refresh access token using a valid refresh token")
async def refresh(token: str):
    user_id = deps.decode_token(token)
    if not user_id:
        raise HTTPException(401, "Invalid refresh")
    return {"access": create_access(user_id), "refresh": token}