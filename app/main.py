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
from app.exceptions import NimadirException, nimadir_error_exc, zero_devision_error_exc


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


#  Exception Handlers
app.add_exception_handler(ZeroDivisionError, zero_devision_error_exc)
app.add_exception_handler(NimadirException, nimadir_error_exc) 