from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, Media
from app.utils import generate_slug
from app.schemas import PostCreateRequest, PostListResponse


app = FastAPI(
    title="Chesnokday achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)


@app.get("/posts/", response_model=list[PostListResponse])
async def get_posts(is_active: bool = None, session: Session = Depends(get_db)):
    stmt = select(Post)

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalar().all()


@app.get("/post/{slug}", response_model=PostListResponse)
async def get_post(slug: str, session: Session = Depends(get_db)):
    stmt = select(Post).where(Post.slug.like(f"%{slug}%"))
    res = session.execute(stmt)
    post = res.scalar().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@app.get("/post/create/")
async def post_create(
    create_data: PostCreateRequest, session: Session = Depends(get_db)
):
    post = Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@app.put("/posts/{post_id}/")
async def post_update(
    post_id: int, update_data: PostCreateRequest, session: Session = Depends(get_db)
):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = update_data.title
    post.body = update_data.body
    post.slug = generate_slug(update_data.title)

    session.commit()
    session.refresh(post)

    return post


@app.patch("/posts/{post_id}/")
async def post_update_patch(
    post_id: int, update_data: PostCreateRequest, session: Session = Depends(get_db)
):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = update_data.title
    post.body = update_data.body
    post.slug = generate_slug(update_data.title)

    session.commit()
    session.refresh(post)

    return post


@app.delete("/posts/{post_id}/")
async def post_delete(post_id: int, session: Session = Depends(get_db)):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()

    return post


@app.deactivate("/posts/{post_id}/")
async def post_deactivate(post_id: int, session: Session = Depends(get_db)):
    post = session.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.is_active = False

    session.commit()
    session.refresh(post)

    return post


################################################################################
################################################################################


@app.get("/media/{media_url}")
async def get_media(media_url: str, session: Session = Depends(get_db)):
    stmt = select(Media)

    # media=session.query(Media).filter(Media.url==media_url).first()

    if not Media:
        raise HTTPException(status_code=404, detail="Media not found")

    res = session.execute(stmt)
    return res.scalar().all()


@app.post("/media/{media_id}")
async def update_media(media_id: int, session: Session = Depends(get_db)):
    media = session.query(Media).filter(Media.url == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    session.commit()
    session.refresh(media)

    return media


@app.delete("/media/{media_id}/")
async def media_delete(media_id: int, session: Session = Depends(get_db)):
    media = session.query(Post).filter(Media.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(media)
    session.commit()

    return media
