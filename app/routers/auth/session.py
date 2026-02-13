import secrets
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select, delete

from app.database import db_dep
from app.models import User, UserSessionToken
from app.dependencies import session_auth_dep
from app.schemas import UserLoginRequest, UserProfileResponse
from app.utils import verify_password
from app.config import settings


router = APIRouter(prefix="/session", tags=["Auth"])


@router.post("/login", status_code=200)
async def login(session: db_dep, login_data: UserLoginRequest, response: Response):
    stmt = select(User).where(User.email == login_data.email)
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password:
        raise HTTPException(status_code=401, detail="Incorrecr password")

    sessionId = secrets.token_urlsafe(32)

    stmt = delete(UserSessionToken).where(UserSessionToken.user_id == user.id)
    session.execute(stmt)
    session.flush()

    new_session = UserSessionToken(
        token=sessionId,
        user_id=user.id,
        expires_at=datetime.now(tz=timezone.utc)
        + timedelta(days=settings.SESSION_ID_EXPIRE_DAYS),
    )
    session.add(new_session)
    session.commit()
    session.refresh(new_session)

    response.set_cookie(
        key="session_id",
        value=sessionId,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.SESSION_ID_EXPIRE_DAYS * 24 * 60 * 60,
    )


@router.get("/profile", response_model=UserProfileResponse)
async def user_profile(session: db_dep, current_user: session_auth_dep):
    return current_user
