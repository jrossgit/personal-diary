import datetime
from sqlalchemy.orm import Session

from diary_api.db_models import Todo, TodoCategory


def db_get_categories(db: Session):
    return db.query(TodoCategory).filter(TodoCategory.deactivate_time is not None).all()


def db_get_category_todos(db: Session, category_id: str, active_only=True):
    query = (
        db.query(Todo)
        .filter(Todo.category_id == category_id)
        .order_by(Todo.create_time.asc())
    )
    if active_only:
        query = query.filter(Todo.complete_time == None)  # noqa: E711
    return query.all()


# TODO: Add tests
def db_get_todo(db: Session, todo_id: str):
    return db.query(Todo).filter(Todo.id == todo_id).one()


def db_create_category(db: Session, name: str):
    category = TodoCategory(name=name)
    db.add(category)
    db.commit()
    return category


def db_get_todos(db: Session, active_only=True):
    query = db.query(Todo).order_by(Todo.create_time.asc())
    if active_only:
        query = query.filter(Todo.complete_time == None)  # noqa: E711
    return query.all()


def db_delete_category_todos(db: Session, id: str):
    category = db.query(TodoCategory).filter_by(id=id).one()
    db.delete(category)
    db.commit()


def db_create_todo(db: Session, category_id: str, text: str):
    todo = Todo(category_id=category_id, text=text)
    db.add(todo)
    db.commit()
    return todo


def db_update_todo(db: Session, todo_id: str, text: Optional[str] = None):
    todo = db_get_todo(db, todo_id=todo_id)
    if text:
        todo.text = text
    db.add(todo)
    db.commit()
    return todo


def db_complete_todo(db: Session, id: str):
    todo = db.query(Todo).filter_by(id=id).one()
    if not todo.complete_time:
        todo.complete_time = datetime.datetime.now()
        db.commit()
    return todo


def db_delete_todo(db: Session, id: str):
    category = db.query(Todo).filter_by(id=id).one()
    db.delete(category)
    db.commit()
