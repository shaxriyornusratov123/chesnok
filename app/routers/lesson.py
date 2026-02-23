from typing import Annotated
from pathlib import Path
import shutil

from fastapi import APIRouter, HTTPException, Header,Form,File, UploadFile
from requests import session
from sqlalchemy import select

from app.database import db_dep
from app.models import User, Media
from app.config import settings
from app.exceptions import NimadirException

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

@router.post("/test_login")
async def test_login(username:Annotated[str, Form()],password: Annotated[str,Form()]):
    return {"username": username, "password": password}

@router.post("/uploadfile")
async def upload_file(file: UploadFile,session: db_dep):
    if file.size > 1024 * 1024 *1 :
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 1MB.")

    file_ext=Path(file.filename).suffix.lower()
    if file_ext not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only jpg, jpeg, and png are allowed.")
    
    path=Path(settings.MEDIA_PATH)
    path.mkdir(exist_ok=True)
    res=path/file.filename
    with open(res, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image=Media(
        url=f"{settings.MEDIA_PATH}/{file.filename}",
    )

    session.add(image)
    session.commit()
    session.refresh(image)

    return {"filename": file.filename,"res":f"{settings.BASE_URL}/{image.url}"}  


@router.get("/exc/")
async def test_exception():
    raise NimadirException("Nimadir xato. Boshqa nom esga kelmadi!")