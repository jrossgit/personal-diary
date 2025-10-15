import datetime
from sqlalchemy.orm import Session

from diary_api.db_models import Todo, TodoCategory


def db_get_categories(db: Session):
    return db.query(TodoCategory).filter(TodoCategory.deactivate_time is not None).all()


def db_get_category_todos(db: Session, category_id: str):
    return (
        db.query(Todo)
        .filter(Todo.complete_time is not None, Todo.category_id == category_id)
        .order_by(Todo.create_time.asc())
    )


def db_get_todos(db: Session):
    return (
        db.query(Todo)
        .filter(Todo.complete_time is not None)
        .order_by(Todo.create_time.asc())
    )


def db_delete_category_todos(db: Session, id: str):
    category = db.query(TodoCategory).filter_by(id=id).one()
    db.delete(category)
    db.commit()


def db_create_todo(db: Session, category_id: str, text: str):
    todo = Todo(category_id=category_id, text=text)
    db.add(todo)
    db.commit()
    return todo


def db_complete_todo(db: Session, id: str):
    todo = db.query(Todo).filter_by(id=id).one()
    todo.complete_time = datetime.datetime.now()
    db.commit()
    return todo


def db_delete_todo(db: Session, id: str):
    category = db.query(Todo).filter_by(id=id).one()
    db.delete(category)
    db.commit()
