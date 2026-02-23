import secrets

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.database import db_dep
from app.models import User
from app.schemas.auth import UserRegisterRequest, UserRegisterResponse
from app.utils import hash_password, send_email, redis_client

router = APIRouter(prefix="/register", tags=["Auth"])


@router.post("/register", response_model=UserRegisterResponse)
async def register_user(session: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = session.execute(stmt).scalars().first()

    if res:
        raise HTTPException(status_code=400, detail="user already exists")

    user = User(
        email=data.email, password_hash=hash_password(data.password), is_active=False
    )

    secret_code = secrets.token_hex(16)
    send_email(
        data.email, "Email confirmation", f"Your confirmation code is {secret_code}"
    )
    redis_client.setex(secret_code, 120, user.email)

    stmt = select(User)
    existing_user = (session.execute(stmt)).scalars().first()

    if not existing_user:
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

    session.add(user)
    session.commit()

    return JSONResponse(
        status_code=204, content={"message": "Email confirmation sent to your email."}
    )


@router.post("verify/{secret_code}", response_model=UserRegisterResponse)
async def verify_register(session: db_dep, secret_code: str):
    email = redis_client.get(secret_code)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid code")

    stmt = select(User).where(User.email == email.decode("utf-8"))
    user = session.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not founded")

    user.is_active = True

    session.commit()

    return JSONResponse(
        status_code=200, content={"message": "User registered successfully"}
    )
