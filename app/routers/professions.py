from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_dep
from app.models import Profession
from app.schemas.professions import (
    ProfessionCreateRequest,
    ProfessionListResponse,
    ProfessionUpdateRequest,
)
from app.dependencies import current_user_basic_dep

router = APIRouter(prefix="/profession", tags=["Profession"])


@router.post("/create/", response_model=ProfessionListResponse)
async def create_profession(session: db_dep, create_data: ProfessionCreateRequest,current_user: current_user_basic_dep):
    if not (current_user.is_superuser or current_user.is_staff):
        raise HTTPException(status_code=403, detail="Not authorized to create a profession  ")

    profession = Profession(name=create_data.name)
    session.add(profession)
    session.commit()
    session.refresh(profession)
    return profession


@router.get("/list/", response_model=list[ProfessionListResponse])
async def profession_list(session: db_dep):
    stmt = select(Profession)
    res = session.execute(stmt).scalars().all()

    return res


@router.put("/update/", response_model=ProfessionListResponse)
async def profession_update(
    session: db_dep, profession_id: int, update_data: ProfessionUpdateRequest,current_user: current_user_basic_dep
):
    if not (current_user.is_superuser or current_user.is_staff):
        raise HTTPException(status_code=403, detail="Not authorized to update this profession  ")

    stmt = select(Profession).where(Profession.id == profession_id)
    res = session.execute(stmt)
    p = res.scalars().first()

    if not p:
        raise HTTPException(status_code=404, detail="Not found")

    p.name = update_data.name
    session.commit()
    session.refresh(p)
    return p


@router.delete("/delete/", status_code=204)
async def profession_delete(session: db_dep, profession_id: int,current_user: current_user_basic_dep):
    if not (current_user.is_superuser or current_user.is_staff):
        raise HTTPException(status_code=403, detail="Not authorized to delete this profession  ")

    stmt = select(Profession).where(Profession.id == profession_id)
    res = session.execute(stmt)
    p = res.scalars().first()

    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(p)
    session.commit()
    return
