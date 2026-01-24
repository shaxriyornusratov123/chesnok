from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Post, Media
from app.database import db_dep
from app.schemas import PostListResponse, PostCreateRequest, PostUpdateRequest
from app.utils import generate_slug

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostListResponse])
async def get_posts(session: db_dep, is_active: bool = None):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalar().all()


@router.get("/{slug}", response_model=PostListResponse)
async def get_post(session: db_dep, slug: str):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalar().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.get("/create/")
async def post_create(session: db_dep, create_data: PostCreateRequest):
    post = Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@router.put("/{post_id}/")
async def post_update(session: db_dep, post_id: int, update_data: PostUpdateRequest):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalar().first()

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
async def post_update(session: db_dep, post_id: int, update_data: PostUpdateRequest):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalar().first()

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


@router.delete("/{post_id}/")
async def post_delete(session: db_dep, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt)
    post = res.scalar().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()


########################################################################
########################################################################


@router.get("/media/{media_id}")
async def get_media(session: db_dep, media_id: int):
    stmt = select(Media).where(Media.id == media_id)
    res = session.execute(stmt)
    media = res.scalar().first()

    if not Media:
        raise HTTPException(status_code=404, detail="Media not found")

    session.commit()
    session.refresh(media)

    return media


@router.post("/media/{media_id}")
async def update_media(session: db_dep, media_id: int):
    media = session.query(Media).filter(Media.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    session.commit()
    session.refresh(media)

    return media


@router.delete("/media/{media_id}/")
async def media_delete(session: db_dep, media_id: int):
    media = session.query(Post).filter(Media.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(media)
    session.commit()

    return media
