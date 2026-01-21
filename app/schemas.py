from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    name: str
    age: int
    is_active: bool | None = None


class UserCreateResponse(BaseModel):
    id: int
    age: int
    is_active: bool
