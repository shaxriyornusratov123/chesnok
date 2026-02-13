from fastapi import FastAPI

from app.routers import (
    auth_router,
    posts_router,
    category_router,
    tag_router,
    user_router,
    comment_router,
    weather_router,
    lesson_router,
    admin_router,
)


app = FastAPI(
    title="Chesnokday achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(posts_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(user_router)
app.include_router(comment_router)
app.include_router(weather_router)
app.include_router(lesson_router)
