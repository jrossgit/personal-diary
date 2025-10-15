import pytest

from tests.setup import create_all, drop_all


@pytest.fixture(autouse=True)
def run_around_tests():
    # runs before and after tests to clear databases, so tests won't conflict
    create_all()
    yield
    drop_all()
