import pytest
from tlm_app import create_app
from tlm_app.database import init_db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    with app.app_context():
        init_db()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
