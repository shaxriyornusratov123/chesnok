from datetime import datetime
import random
import string

from fastapi import FastAPI
from fastapi import status
from fastapi.responses import JSONResponse

app = FastAPI()
users_db = dict()
news_db = dict()
category_db = dict()


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choices(characters, k=length))
    return random_string


@app.post("/users/create/")
def user_create():
    user_id = random.randrange(1, 10000)
    name = generate_random_string(10)
    age = random.randint(1, 60)
    is_active = random.choice([True, False])

    new_user = {
        "id": user_id,
        "name": name,
        "age": age,
        "is_active": is_active,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    users_db[user_id] = new_user
    return new_user


@app.get("/users/list/")
def users_list():
    return users_db


@app.get("/users/{user_id}/")
def users_detail(user_id: int):
    try:
        return users_db[user_id]
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.put("/users/{user_id}/")
def user_update(user_id: int):
    try:
        user = users_db[user_id]
        user["name"] = generate_random_string(10)
        user["age"] = random.randint(1, 60)
        users_db[user_id] = user

        return user
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.delete("/users/{user_id}/")
def user_delete(user_id: int):
    try:
        del users_db[user_id]
        return JSONResponse(status_code=204)
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.get("/users/active/")
def get_active_users():
    return [user for user in users_db.values() if user["is_active"]]


@app.get("/news")
def get_news(page: int = 1):
    return {"page": page, "message": f"№{page}"}


@app.get("/home")
def return_home():
    return {"page": 1}


@app.get("/category")
def categories():
    return [
        {"id": 1, "name": "O'zbekiston"},
        {"id": 2, "Jahon": "Jahon"},
        {"id": 3, "Iqtisodiyot": "Iqtisodiyot"},
        {"id": 4, "Sport": "Sport"},
    ]


@app.get("/news/{news_id}")
def news(news_id: int):
    return news_db[news_id]


@app.delete("/news/{news_id}/")
def news_delete(news_id: int):
    try:
        del news_db[news_id]
        return JSONResponse(status_code=204)
    except KeyError:
        return JSONResponse(
            content={"error": "news not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.post("/news/create/")
def news_create():
    news_id = random.randrange(1, 10000)
    title = generate_random_string(50)
    name = generate_random_string(10)

    new_news = {
        "id": news_id,
        "title": title,
        "name": name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    news_db[news_id] = new_news
    return new_news


@app.post("/categories/create")
def create_category():
    news_id = random.randrange(1, 10000)
    name = generate_random_string(10)

    new_category = {
        "id": news_id,
        "name": name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return new_category


@app.post("/comment")
def comment(comment: str):
    return {"massege": "commentariya qo'shildi", "comment": comment}


@app.put("/news/{news_id}")
def news_update(news_id: int):
    try:
        news = news_db[news_id]
        news["name"] = generate_random_string(10)
        news["title"] = generate_random_string(50)
        users_db[news_id] = news

        return news
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.put("/category/{category_id}")
def category_update(category_id: int):
    try:
        category = category_db[category_id]
        category["name"] = generate_random_string(10)
        category_db[category_id] = category

        return category
    except KeyError:
        return JSONResponse(
            content={"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )


@app.patch("/news/{news_id}/status")
def update_news_status(news_id: int, status: str):
    if news_id not in news_db:
        return {"error": "Not founded"}

    news_db[news_id]["status"] = status
    return {"message": "status uzgartirildi", "news": news_db[news_id]}


@app.patch("/user/{user_id}/name")
def update_user_name(user_id: int, name: str):
    if user_id not in users_db:
        return {"error": "user not founded"}

    users_db[user_id]["name"] = name
    return {"message": "ism uzgartirildi", "user": users_db[user_id]}
