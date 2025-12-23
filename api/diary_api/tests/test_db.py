from datetime import datetime, timedelta
import pytest

from diary_api.db_models import Todo, TodoCategory
from diary_api.tests.factories import (
    CompleteTodoFactory,
    TodoCategoryFactory,
    TodoFactory,
)
from diary_api.tests.setup import create_all, drop_all, test_db
from diary_api.db import (
    db_complete_todo,
    db_create_category,
    db_create_todo,
    db_delete_category_todos,
    db_delete_todo,
    db_get_categories,
    db_get_category_todos,
    db_get_todos,
)


@pytest.fixture(autouse=True)
def run_around_tests():
    # runs before and after tests to clear databases, so tests won't conflict
    create_all()
    yield
    drop_all()


def _assert_id_retrieve_order(source, test_target, desired_order):
    print([item.id for item in source])
    required_ids = [source[i].id for i in desired_order]
    assert [item.id for item in test_target] == required_ids


def test_create_category():

    category = db_create_category(test_db, "Cool tasks")
    assert category.id
    assert category.create_time
    assert category.name == "Cool tasks"


def test_get_categories_gets_all_categories():
    category = TodoCategoryFactory()

    categories_db = db_get_categories(test_db)

    assert len(categories_db) == 1
    assert categories_db[0].id == category.id


def test_get_category_todos_gets_all_todos_in_category():
    c1, _, c2 = [
        TodoCategoryFactory(name="Cat 1"),
        TodoCategoryFactory(name="Empty Category"),
        TodoCategoryFactory(name="Cat 2"),
    ]
    todos = [
        TodoFactory(category=c1),
        TodoFactory(category=c2),
        CompleteTodoFactory(category=c2),
    ]

    _assert_id_retrieve_order(
        todos, list(db_get_category_todos(test_db, c1.id, active_only=False)), [0]
    )
    _assert_id_retrieve_order(
        todos, list(db_get_category_todos(test_db, c2.id, active_only=False)), [1, 2]
    )
    _assert_id_retrieve_order(
        todos, list(db_get_category_todos(test_db, c2.id, active_only=True)), [1]
    )


def test_db_get_todos_gets_all_complete_todos_filters_by_active():
    c1, _, c2 = [
        TodoCategoryFactory(name="Cat 1"),
        TodoCategoryFactory(name="Empty Category"),
        TodoCategoryFactory(name="Cat 2"),
    ]
    _ = [
        TodoFactory(category=c1),
        TodoFactory(category=c2),
        CompleteTodoFactory(category=c2),
    ]

    db_todos = db_get_todos(test_db)
    assert len(db_todos) == 2


def test_db_get_todos_gets_all_complete_todos_accepts_non_active_todos_when_requested():
    c1, _, c2 = [
        TodoCategoryFactory(name="Cat 1"),
        TodoCategoryFactory(name="Empty Category"),
        TodoCategoryFactory(name="Cat 2"),
    ]
    _ = [
        TodoFactory(category=c1),
        TodoFactory(category=c2),
        CompleteTodoFactory(category=c2),
    ]

    db_todos = db_get_todos(test_db, active_only=False)
    assert len(db_todos) == 3


def test_db_get_todos_orders_by_timestamp():
    c1, _, c2 = [
        TodoCategoryFactory(name="Cat 1"),
        TodoCategoryFactory(name="Empty Category"),
        TodoCategoryFactory(name="Cat 2"),
    ]
    _ = [
        TodoFactory(category=c1),
        TodoFactory(category=c2),
        CompleteTodoFactory(category=c2),
    ]

    db_todos = db_get_todos(test_db)
    assert db_todos[1].create_time >= db_todos[0].create_time


def test_delete_category_deletes_category():
    c1, c2 = [
        TodoCategoryFactory(name="Cat 1"),
        TodoCategoryFactory(name="Cat 2"),
    ]

    db_delete_category_todos(test_db, c1.id)
    current_todo = test_db.query(TodoCategory).one()
    assert current_todo.id == c2.id

    db_delete_category_todos(test_db, c2.id)
    assert not test_db.query(TodoCategory).count()


def test_create_todo():
    cat = TodoCategoryFactory()

    todo = db_create_todo(test_db, cat.id, "Do the thing!")
    assert todo.create_time
    assert not todo.complete_time
    assert todo.text == "Do the thing!"
    assert todo.category_id == cat.id


def test_complete_todo_fills_in_complete_time_as_now():
    todo = TodoFactory()

    db_complete_todo(test_db, todo.id)
    assert todo.complete_time
    assert datetime.now() - todo.complete_time < timedelta(seconds=1)


def test_complete_todo_does_nothing_if_already_complete():
    todo = CompleteTodoFactory()
    complete_time = todo.complete_time

    db_complete_todo(test_db, todo.id)
    assert todo.complete_time
    assert todo.complete_time == complete_time


def test_delete_todo():
    todo = TodoFactory()
    db_delete_todo(test_db, todo.id)
    assert len(test_db.query(Todo).all()) == 0
