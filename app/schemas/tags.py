from pydantic import BaseModel


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
