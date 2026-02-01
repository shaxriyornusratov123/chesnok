from datetime import datetime

from pydantic import BaseModel


class CommentCreateRequest(BaseModel):
    user_id: int
    text: str
    post_id: int


class CommentListresponse(BaseModel):
    id: int
    user_id: int
    text: str
    post_id: int
    is_active: bool
    created_at: datetime
    update_at: datetime


class CommentUpdateRequest(BaseModel):
    text: str | None = None
    is_active: bool | None = None
