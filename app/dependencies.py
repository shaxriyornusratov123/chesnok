from typing import Annotated
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import db_dep
from app.models import User, UserSessionToken
from app.utils import verify_password

basic = HTTPBasic()
basic_auth_dep = Annotated[HTTPBasicCredentials, Depends(basic)]


def get_current_user(session: db_dep, credentials: basic_auth_dep):
    stmt = (
        select(User)
        .where(User.email == credentials.username)
        .options(joinedload(User.profession))
    )
    user = session.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password:
        raise HTTPException(status_code=401, detail="incorrect password")


current_user_basic_dep = Annotated[User, Depends(get_current_user)]


def get_current_user_session(session: db_dep, request: Request):
    sessionId = request.cookies.get("session_id")
    if not sessionId:
        raise HTTPException(status_code=401, detail="Not authenticated")

    stmt = select(UserSessionToken).where(UserSessionToken.token == sessionId)
    session_obj = session.execute(stmt).scalars().first()

    if not session_obj:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session_obj.expires_at < datetime.now(tz=timezone.utc):
        session.delete(session_obj)
        session.commit()
        raise HTTPException(status_code=401, detail="Not authenticated")

    stmt = (
        select(User)
        .where(User.id == session_obj.user_id)
        .options(joinedload(User.profession))
    )
    user = session.execute(stmt).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not founded")

    return user


session_auth_dep = Annotated[User, Depends(get_current_user_session)]
