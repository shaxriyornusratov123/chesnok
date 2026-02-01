from pydantic import BaseModel


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
