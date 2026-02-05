from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select

from app.database import db_dep
from app.models import User
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse
from app.utils import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

basic = HTTPBasic()


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(session: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = session.execute(stmt).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="user already exists")

    user = User(email=data.email, password=hash_password(data.password))

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post("/login/")
async def login_user(
    session: db_dep, credentials: Annotated[HTTPBasicCredentials, Depends(basic)]
):
    print(">>>", credentials.username, credentials.password)
    stmt = select(User).where(User.email == credentials.username)
    user = session.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user
