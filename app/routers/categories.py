from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Category
from app.database import db_dep
from app.schemas import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
    CategoryListResponse,
)
from app.utils import generate_slug

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/list/", response_model=list[CategoryListResponse])
async def get_post_list(session: db_dep):
    stmt = select(Category)
    res = session.execute(stmt)
    category = res.scalars().all()

    if not category:
        raise HTTPException(status_code=404, detail="Post not found")

    return category


@router.get("/{slug}/", response_model=CategoryListResponse)
async def get_post(session: db_dep, slug: str):
    stmt = select(Category).where(Category.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    category = res.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="Post not found")

    return category


@router.post("/create/", response_model=CategoryCreateRequest)
async def create_category(session: db_dep, create_data: CategoryCreateRequest):
    category = Category(name=create_data.name, slug=generate_slug(create_data.name))

    session.add(category)
    session.commit()
    session.refresh(category)

    return category


@router.put("/{categy_id}", response_model=CategoryUpdateRequest)
async def update_category_put(
    session: db_dep, category_id: int, update_data: CategoryUpdateRequest
):
    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt)
    category = res.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = update_data.name
    category.slug = generate_slug(update_data.name)

    session.commit()
    session.refresh(category)

    return category


@router.patch("/{categy_id}", response_model=CategoryUpdateRequest)
async def update_category(
    session: db_dep, category_id: int, update_data: CategoryUpdateRequest
):
    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt)
    category = res.scalar().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = update_data.name
    category.slug = generate_slug(update_data.name)

    session.commit()
    session.refresh(category)

    return category


@router.delete("/{category_id}")
async def delete_category(session: db_dep, category_id: int):
    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt)
    category = res.scalar().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    session.delete(category)
    session.commit()
