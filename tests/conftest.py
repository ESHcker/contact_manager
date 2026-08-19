import pytest
from conelman import create_app
from conelman.models import User, Contact
from conelman.db import get_db
from werkzeug.security import generate_password_hash

#Create test db and app
@pytest.fixture
def app():
    test_config = {
        'SQLALCHEMY_ENGINES': {"default": "sqlite:///:memory:"},
        'TESTING': True
    }
    app = create_app(test_config)

    yield app

#Create client for tests
@pytest.fixture
def client(app):
    return app.test_client()

#Create user in database for tests
@pytest.fixture
def seed_user(app, client):
    with app.app_context():
        user_test = User(username='test',password=generate_password_hash('test'))
        get_db().session.add(user_test)
        get_db().session.commit()

    return user_test

@pytest.fixture
def seed_contacts(app, client):
    with app.app_context():
        contact_test = Contact(name = 'illojuan', phone = '928247364', notes="streamer", user_id = 1)
        get_db().session.add(contact_test)
        get_db().session.commit()
    
    return contact_test

#Easy functions for login and logout tests
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
