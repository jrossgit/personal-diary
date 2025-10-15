import datetime
import logging

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

from diary_api.db import db_complete_todo, db_create_todo, db_delete_category_todos, db_delete_todo, db_get_categories, db_get_category_todos, db_get_todos
from diary_api.deps.db import DBSession

app = FastAPI()
LOGGER = logging.getLogger(__name__)


class TodoWrite(BaseModel):
    text: str


class TodoRead(TodoWrite):
    id: str
    category_id: str
    create_time: datetime.datetime


class CategoryListRead(BaseModel):
    id: str
    name: str
    create_time: datetime.datetime


class CategoryDetailRead(CategoryListRead):
    todos: list[TodoRead]


@app.get("/categories")
def route_get_categories(db: DBSession, background_tasks: BackgroundTasks) -> list[CategoryListRead]:
    return db_get_categories(db)


@app.get("/categories/{id}/todos")
def route_get_category_todos(db: DBSession, id: str) -> list[TodoRead]:
    return db_get_category_todos(db, id)


@app.delete("/categories/{id}")
def route_delete_category(db: DBSession, id: str) -> None:
    db_delete_category_todos(db, id)


@app.post("/categories/{category_id}/todos")
def route_create_todo(db: DBSession, todo: TodoWrite, category_id: str) -> TodoRead:
    return db_create_todo(db, category_id, todo.text)


@app.get("/todos")
def route_get_todos(db: DBSession) -> list[TodoRead]:
    return db_get_todos(db)


@app.post("/todos/{todo_id}:complete")
def route_todo_complete(db: DBSession, todo_id: str) -> None:
    return db_complete_todo(db, todo_id)


@app.delete("/todos/{id}")
def route_delete_todo(db: DBSession, id: str) -> None:
    db_delete_todo(db, id)
