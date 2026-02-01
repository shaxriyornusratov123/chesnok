from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    password_hash: str
    first_name: str
    last_name: str
    profession_id: int
    bio: str
    is_active: bool
    is_staff: bool
    is_superuser: bool


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    password_hash: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None


class UserListResponse(BaseModel):
    id: int
    email: EmailStr
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
