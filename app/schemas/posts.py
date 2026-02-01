from datetime import datetime

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    user_id: int
    title: str
    body: str
    category_id: int | None = None
    created_at: datetime | None = None


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    is_active: bool
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 6,
                    "title": "O'zbekistonning YaIM si 130 mlrddan oshdi.",
                    "slug": "ozbekistonning-yaim-si-130-mlrddan-oshdi",
                    "body": "O'zbekiston Markaziy Osiyodagi eng kuchli davlat boldi",
                    "is_active": True,
                    "created_at": "2026-01-19T13:01:18.001Z",
                }
            ]
        }
    }


class PostUpdateRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    is_active: bool | None = None
