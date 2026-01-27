from .posts import router as posts_router
from .categories import router as category_router
from .tags import router as tag_router
from .users import router as user_router

__all__ = ["posts_router", "category_router", "tag_router", "user_router"]
