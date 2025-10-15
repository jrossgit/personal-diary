import factory
from diary_api import db_models
from tests.setup import test_db
# from diary_api.deps.db import get_db


class TodoCategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = db_models.TodoCategory
        sqlalchemy_session = test_db
        sqlalchemy_session_persistence = "commit"

    name = "Test Category"
