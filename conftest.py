import pytest
from app import create_app
from app.services import user_service


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    user_service.reset_users()
    with app.test_client() as c:
        yield c
    user_service.reset_users()
