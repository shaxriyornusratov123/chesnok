from fastapi import APIRouter

from app.models import Comment
from app.database import db_dep
from app.schemas import CommentCreateRequest


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/create/")
async def create_comment(session: db_dep, create_data: CommentCreateRequest):
    comment = Comment(
        user_id=create_data.user_id, text=create_data.text, post_id=create_data.post_id
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment
