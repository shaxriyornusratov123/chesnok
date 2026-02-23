from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select

from app.models import Post, PostTag, Tag
from app.database import db_dep
from app.schemas.posts import PostListResponse, PostCreateRequest, PostUpdateRequest
from app.utils import generate_slug
from app.dependencies import current_user_basic_dep

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


# @router.get("/{author_id}", response_model=list[PostListResponse])
# async def filter_posts_by_author(session: db_dep, author_id: int):
#     stmt = select(Post).join(User, Post.user_id == User.id)

#     if author_id:
#         stmt = stmt.where(
#             User.id == author_id and User.is_staff == True & User.is_active == True
#         )
#         stmt = stmt.order_by(Post.created_at.desc())
#         res = session.execute(stmt)
#         return res.scalars().all()


@router.get("/trending/", response_model=list[PostListResponse])
async def get_trending_posts(session: db_dep):
    stmt = (
        select(Post)
        .where(Post.created_at >= datetime.now() - timedelta(days=7))
        .order_by(Post.likes_count.desc())
        .limit(5)
    )
    res = session.execute(stmt)
    post = res.scalars().all()
    return post


@router.get("/{slug}", response_model=PostListResponse)
async def get_post(session: db_dep, slug: str):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.get("/search/", response_model=list[PostListResponse])
async def search_posts(session: db_dep, key_word: str):
    stmt = select(Post).where(Post.title.ilike(f"%{key_word}%"))
    res = session.execute(stmt)
    posts = res.scalars().all()
    return posts


@router.post("/create/")
async def post_create(
    session: db_dep,
    create_data: PostCreateRequest,
    current_user: current_user_basic_dep,
):
    if not (current_user.is_superuser or current_user.is_staff):
        raise HTTPException(status_code=403, detail="Not authorized to create a post  ")

    post = Post(
        user_id=current_user.id,
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
async def post_update(
    session: db_dep,
    post_id: int,
    update_data: PostUpdateRequest,
    current_user: current_user_basic_dep,
):
    if not (current_user.is_superuser or current_user.id == post_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this post  "
        )

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


@router.post("/like/{post_id}")
async def add_like(session: db_dep, post_id: int, request: Request):
    stmt = select(Post).where(Post.id == post_id)
    post = session.execute(stmt).scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.likes_count += 1
    session.commit()
    return {"status": "success", "total_count": post.likes_count}


@router.patch("/{post_id}/")
async def post_update_patch(
    session: db_dep,
    post_id: int,
    update_data: PostUpdateRequest,
    current_user: current_user_basic_dep,
):
    if not (current_user.is_superuser or current_user.id == post_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to update this post  "
        )

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
async def post_delete(
    session: db_dep, post_id: int, current_user: current_user_basic_dep
):
    if not (current_user.is_superuser or current_user.id == post_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this post  "
        )

    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()
