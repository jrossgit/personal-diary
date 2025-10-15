import pytest

from tests.factories import TodoCategoryFactory
from tests.setup import create_all, drop_all, test_db
from diary_api.db import db_get_categories


@pytest.fixture(autouse=True)
def run_around_tests():
    # runs before and after tests to clear databases, so tests won't conflict
    create_all()
    yield
    drop_all()


def test_get_categories_gets_all_categories():
    category = TodoCategoryFactory()

    categories_db = db_get_categories(test_db)

    assert len(categories_db) == 1
    assert categories_db[0].id == category.id
