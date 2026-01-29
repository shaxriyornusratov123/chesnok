from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Post, PostTag, Tag, User
from app.database import db_dep
from app.schemas import PostListResponse, PostCreateRequest, PostUpdateRequest
from app.utils import generate_slug

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostListResponse])
async def get_posts_list(
    session: db_dep,
    is_active: bool | None = None,
    category_id: int | None = None,
    tag_id: int | None = None,
):
    stmt = (
        select(Post)
        .join(PostTag, Post.id == PostTag.post_id)
        .join(Tag, PostTag.tag_id == Tag.id)
    )

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    if category_id:
        stmt = stmt.where(Post.category_id == category_id)

    if tag_id:
        stmt = stmt.where(Tag.id == tag_id)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()


@router.get("/{user_id}", response_model=list[PostListResponse])
async def filter_posts_by_author(session: db_dep, user_id: int):
    stmt = select(Post).join(User, Post.user_id == User.id)

    if user_id:
        stmt = stmt.where(User.id == user_id)
        stmt = stmt.order_by(Post.created_at.desc())
        res = session.execute(stmt)
        return res.scalars().all()


@router.get("/{slug}", response_model=PostListResponse)
async def get_post(session: db_dep, slug: str):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.get("/{created_at}/", response_model=list[PostListResponse])
async def get_posts_by_created_at(session: db_dep, created_at: datetime):
    stmt = select(Post).where(Post.created_at == created_at)
    res = session.execute(stmt)
    posts = res.scalars().all()
    return posts


@router.get("/{mins_read}/", response_model=list[PostListResponse])
async def get_posts_by_mins_read(session: db_dep, mins_read: int):
    stmt = select(Post).where(Post.mins_read == mins_read)
    res = session.execute(stmt)
    posts = res.scalars().all()
    return posts


@router.get("/{likes_count}/", response_model=list[PostListResponse])
async def get_posts_by_likes_count(session: db_dep, likes_count: int):
    stmt = select(Post).where(Post.likes_count == likes_count)
    res = session.execute(stmt)
    posts = res.scalars().all()
    return posts


@router.post("/create/")
async def post_create(session: db_dep, create_data: PostCreateRequest):
    post = Post(
        user_id=create_data.user_id,
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
        category_id=create_data.category_id,
        created_at=create_data.created_at,
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@router.put("/{post_id}/")
async def post_update(session: db_dep, post_id: int, update_data: PostUpdateRequest):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.titlez:
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body:
        post.body = update_data.body

    if update_data.is_active:
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)

    return post


@router.patch("/{post_id}/")
async def post_update_patch(
    session: db_dep, post_id: int, update_data: PostUpdateRequest
):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.title:
        post.title = update_data.title
        post.slug = generate_slug(update_data.title)

    if update_data.body:
        post.body = update_data.body

    if update_data.is_active:
        post.is_active = update_data.is_active

    session.commit()
    session.refresh(post)

    return post


@router.delete("/{post_id}/")
async def post_delete(session: db_dep, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()
