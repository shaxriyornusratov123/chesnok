from datetime import datetime

from pydantic import BaseModel, EmailStr, model_validator
from zxcvbn import zxcvbn

from app.schemas.common import ProfessionInline


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    password2: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegisterRequest":
        if self.password != self.password2:
            raise ValueError("passwords do not match")

        if len(self.password) < 8:
            raise ValueError("password must be at least 8 characters long")

        if zxcvbn(self.password) and zxcvbn(self.password)["score"] < 2:
            raise ValueError("password is weak")
        return self


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    posts_count: int
    posts_read_count: int
    profession: ProfessionInline | None = None
    is_active: bool
    is_staff: bool
    is_superuser: bool
    is_deleted: bool


class UserProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    profession_id: int | None = None
