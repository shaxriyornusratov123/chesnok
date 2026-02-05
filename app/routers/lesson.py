from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import select

from app.database import db_dep
from app.models import User

router = APIRouter(prefix="/lesson", tags=["lesson"])

SECRET_TOKEN = "toshmat"


@router.get("/protected/")
async def protected_api(session: db_dep, email: str, X_chesnok_token: str = Header()):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="No chsenok token.")

    if X_chesnok_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Incorrect chesnok token.")

    stmt = select(User).where(User.email == email)
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        HTTPException(status_code=404, detail="user not founded")

    return user


@router.get("/protected/adminonly")
async def protected_admin(session: db_dep, email: str, X_chesnok_token: str = Header()):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="No chsenok token.")

    if X_chesnok_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Incorrect chesnok token.")

    stmt = select(User).where(User.email == email)
    res = session.execute(stmt)
    user = res.scalars().first()

    if not user:
        HTTPException(status_code=404, detail="user not founded")

    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="buni kurishga seni haqqing yo'q! ")

    return user
