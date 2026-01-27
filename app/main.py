from fastapi import FastAPI

from app.routers import posts_router, category_router, tag_router, user_router


app = FastAPI(
    title="Chesnokday achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
app.include_router(category_router)
app.include_router(tag_router)
app.include_router(user_router)
