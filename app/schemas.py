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


class CategoryCreateRequest(BaseModel):
    name: str
    slug: str


class CategoryUpdateRequest(BaseModel):
    name: str | None = None


class CategoryListResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {
        "json_schema_extra": {"examples": [{"id": 5, "name": "SPORT", "slug": "sport"}]}
    }


class TagCreateRequest(BaseModel):
    name: str
    slug: str


class TagUpdateRequest(BaseModel):
    name: str | None = None


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"id": 5, "name": "SIYOSAT", "slug": "siyosat"}]
        }
    }


class UserCreateRequest(BaseModel):
    email: str
    password_hash: str
    first_name: str
    last_name: str
    profession_id: int
    bio: str
    is_active: bool
    is_staff: bool
    is_superuser: bool


class UserUpdateRequest(BaseModel):
    email: str | None = None
    password_hash: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None


class UserListResponse(BaseModel):
    id: int
    email: str
    password_hash: str
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 5,
                    "email": "eshmat@gmail.com",
                    "password_hash": "Eshmat01",
                    "first_name": "Eshmat",
                    "last_name": "Toshmatov",
                    "bio": "5 yil tajribaga ega jurnalist",
                    "is_active": True,
                    "is_staff": False,
                    "is_superuser": False,
                    "created_at": "2026-01-19T13:01:18.001Z",
                }
            ]
        }
    }


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
