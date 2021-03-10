import os
# import tempfile

import pytest
import config
from app import create_app
from app.models import db
# from app.db import get_db
# from app.db import init_db

# read in SQL for populating test data
# with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#     _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    PWD = os.environ.get('APP_PWD')
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    # app = create_app({"TESTING": True, "DATABASE": db_path})
    from shutil import copyfile
    copyfile(f'{PWD}/tests/database/voca.db', f'{PWD}/tests/test.db')
    app = create_app()
    # app.config
    app.config.from_object(config.TestingConfig)
    # create the database and load test data
    with app.app_context():
        db.init_app(app)

    yield app
    os.remove(f'{PWD}/tests/test.db')


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="truong", password="1234"):
        # print(password)
        return self._client.post(
            "/login", data={"username": username, "password": password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)
