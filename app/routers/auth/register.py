from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import User
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse
from app.utils import hash_password

router = APIRouter(prefix="/register", tags=["Auth"])


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(session: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = session.execute(stmt).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="user already exists")

    user = User(email=data.email, password_hash=hash_password(data.password))

    stmt = select(User)
    existing_user = (session.execute(stmt)).scalars().first()

    if not existing_user:
        user.is_staff = True
        user.is_superuser = True

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
