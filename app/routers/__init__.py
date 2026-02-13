from .posts import router as posts_router
from .categories import router as category_router
from .tags import router as tag_router
from .users import router as user_router
from .comments import router as comment_router
from .weather import router as weather_router
from .auth import auth_router
from .lesson import router as lesson_router
from .admin import router as admin_router

__all__ = [
    "posts_router",
    "category_router",
    "tag_router",
    "user_router",
    "comment_router",
    "weather_router",
    "auth_router",
    "lesson_router",
    "admin_router",
]
