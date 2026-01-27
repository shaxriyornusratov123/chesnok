from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import User
from app.database import db_dep
from app.schemas import UserCreateRequest, UserListResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/list/", response_model=list[UserListResponse])
async def get_users_list(session: db_dep):
    stmt = select(User)
    res = session.execute(stmt)
    user = res.scalars().all()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/{name}/", response_model=UserListResponse)
async def get_user(session: db_dep, name: str):
    stmt = select(User).where(User.first_name.ilike(f"%{name}%"))
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/", response_model=list[UserListResponse])
async def get_all_users(session: db_dep, is_active: bool = None):
    stmt = select(User)

    if is_active is not None:
        stmt = stmt.where(User.is_active == is_active)

    stmt = stmt.order_by(User.id.desc())
    res = session.execute(stmt)
    return res.scalars().all()


@router.get("/{created_at}", response_model=list[UserListResponse])
async def get_users_by_created_at(session: db_dep, created_at: datetime):
    stmt = select(User).where(User.created_at == created_at)
    res = session.execute(stmt)
    return res.scalars().all()


@router.get("/{posts_count}/", response_model=list[UserListResponse])
async def get_users_by_posts_count(session: db_dep, posts_count: int):
    stmt = select(User).where(User.posts_count == posts_count)
    res = session.execute(stmt)
    return res.scalars().all()


@router.post("/create/")
async def create_user(session: db_dep, create_data: UserCreateRequest):
    user = User(
        email=create_data.email,
        password_hash=create_data.password_hash,
        first_name=create_data.first_name,
        last_name=create_data.last_name,
        profession_id=create_data.profession_id,
        bio=create_data.bio,
        is_active=create_data.is_active,
        is_staff=create_data.is_staff,
        is_superuser=create_data.is_superuser,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.put("/{user_id}/")
async def update_user(session: db_dep, user_id: int, update_data: UserUpdateRequest):
    stmt = select(User).where(User.id == user_id)
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if update_data.email:
        user.email = update_data.email
    if update_data.password_hash:
        user.password_hash = update_data.password_hash
    if update_data.first_name:
        user.first_name = update_data.first_name
    if update_data.last_name:
        user.last_name = update_data.last_name
    if update_data.bio:
        user.bio = update_data.bio
    if update_data.is_active:
        user.is_active = update_data.is_active
    if update_data.is_staff:
        user.is_staff = update_data.is_staff
    if update_data.is_superuser:
        user.is_superuser = update_data.is_superuser

    session.commit()
    session.refresh(user)

    return user


@router.delete("/{user_id}/")
async def delete_user(session: db_dep, user_id: int):
    stmt = select(User).where(User.id == user_id)
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
