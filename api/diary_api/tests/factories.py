import datetime
import factory
from diary_api import db_models
from diary_api.tests.setup import test_db
# from diary_api.deps.db import get_db


class TodoCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = db_models.TodoCategory
        sqlalchemy_session = test_db
        sqlalchemy_session_persistence = "commit"

    name = "Test Category"


class TodoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = db_models.Todo
        sqlalchemy_session = test_db
        sqlalchemy_session_persistence = "commit"

    text = "Test Todo"
    category = TodoCategoryFactory


class CompleteTodoFactory(TodoFactory):
    class Meta:
        model = db_models.Todo
        sqlalchemy_session = test_db
        sqlalchemy_session_persistence = "commit"

    text = "Test Todo"
    category = TodoCategoryFactory
    complete_time = datetime.datetime.now()
