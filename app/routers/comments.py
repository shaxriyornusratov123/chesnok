from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Comment
from app.database import db_dep
from app.schemas.comments import (
    CommentCreateRequest,
    CommentListResponse,
    CommentUpdateRequest,
)
from app.dependencies import current_user_basic_dep

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{comment_id}", response_model=list[CommentListResponse])
async def get_comment(session: db_dep, comment_id: int):
    stmt = select(Comment).where(Comment.id == comment_id)
    res = session.execute(stmt)
    comment = res.scalars().first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.post("/create/")
async def create_comment(session: db_dep, create_data: CommentCreateRequest):
    comment = Comment(
        user_id=create_data.user_id, text=create_data.text, post_id=create_data.post_id
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment


@router.put("/{comment_id}")
async def update_comment(
    session: db_dep, comment_id: int, update_data: CommentUpdateRequest
):
    stmt = select(Comment).where(Comment.id == comment_id)
    res = session.execute(stmt)
    comment = res.scalars().first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if update_data.text:
        comment.text = update_data.text

    if update_data.is_active:
        comment.is_active = update_data.is_active

    return comment


@router.delete("/{comment_id}")
async def delete_comment(
    session: db_dep, comment_id: int, current_user: current_user_basic_dep
):
    if not (current_user.is_superuser or current_user.id == comment_id):
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this comment  "
        )

    stmt = select(Comment).where(Comment.id == comment_id)
    res = session.execute(stmt)
    comment = res.scalars().first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    session.delete(comment)
    session.commit()
