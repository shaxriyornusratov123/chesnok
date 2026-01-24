from fastapi import FastAPI

from app.routers import posts_router


app = FastAPI(
    title="Chesnokday achchiq yangiliklar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
