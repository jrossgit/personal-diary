import datetime
import logging

from diary_api.deps.config import get_settings
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from diary_api.db import (
    db_complete_todo,
    db_create_category,
    db_create_todo,
    db_delete_category_todos,
    db_delete_todo,
    db_get_categories,
    db_get_category_todos,
    db_get_todos,
    db_update_todo,
)
from diary_api.deps.db import DBSession


app = FastAPI()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoWrite(BaseModel):
    text: str


class TodoRead(TodoWrite):
    id: str
    category_id: str
    create_time: datetime.datetime


class CategoryWrite(BaseModel):
    name: str


class CategoryListRead(CategoryWrite):
    id: str
    create_time: datetime.datetime


class CategoryDetailRead(CategoryListRead):
    todos: list[TodoRead]


@app.get("/categories")
def route_get_categories(
    db: DBSession
) -> list[CategoryListRead]:
    return db_get_categories(db)


@app.post("/categories")
def route_create_category(
    db: DBSession,
    category_in: CategoryWrite,
) -> CategoryDetailRead:
    return db_create_category(db, category_in.name)


@app.get("/categories/{id}/todos")
def route_get_category_todos(db: DBSession, id: str) -> list[TodoRead]:
    return db_get_category_todos(db, id)


@app.delete("/categories/{id}")
def route_delete_category(db: DBSession, id: str) -> None:
    db_delete_category_todos(db, id)


@app.post("/categories/{category_id}/todos")
def route_create_todo(db: DBSession, todo: TodoWrite, category_id: str) -> TodoRead:
    return db_create_todo(db, category_id, todo.text)


@app.patch("/todos/{todo_id}")
def route_update_todo(db: DBSession, todo: TodoWrite, todo_id: str) -> TodoRead:
    return db_update_todo(db, todo_id, todo.text)


@app.get("/todos")
def route_get_todos(db: DBSession) -> list[TodoRead]:
    return db_get_todos(db)


@app.post("/todos/{todo_id}:complete")
def route_todo_complete(db: DBSession, todo_id: str) -> None:
    return db_complete_todo(db, todo_id)


@app.delete("/todos/{id}")
def route_delete_todo(db: DBSession, id: str) -> None:
    db_delete_todo(db, id)
