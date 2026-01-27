from datetime import datetime

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    title: str
    body: str


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    is_active: bool
    created_at: datetime


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


class TagCreateRequest(BaseModel):
    name: str
    slug: str


class TagUpdateRequest(BaseModel):
    name: str | None = None


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str


class UserCreateRequest(BaseModel):
    email: str
    password_hash: str
    first_name: str
    last_name: str
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
    email: str
    password_hash: str
    first_name: str
    last_name: str
    bio: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
