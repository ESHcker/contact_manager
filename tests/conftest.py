import pytest
from conelman import create_app
from conelman.models import User
from conelman.db import get_db
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    test_config = {
        'SQLALCHEMY_ENGINES': {"default": "sqlite:///:memory:"},
        'TESTING': True
    }
    app = create_app(test_config)

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seed_user(app, client):
    with app.app_context():
        user_test = User(username='test',password=generate_password_hash('test'))
        get_db().session.add(user_test)
        get_db().session.commit()

    return user_test

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
