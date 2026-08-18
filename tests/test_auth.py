import pytest

from flask import g, session
from conelman.db import get_db
from conelman.models import User
from sqlalchemy import select

#Test register-----
def test_register(client,app):
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        'auth/register', data={'username' : 'test', 'password' : 'test'}
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().session.scalars(
                select(User).where(User.username == 'test')
        ).first() is not None

@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('', 'a', b'Username is required'),
    ('a', '', b'Password is required'),
    ('test', 'test', b'already registered'),
))
def test_register_user_input(client, seed_user, username, password, message):
    response = client.post(
        'auth/register', data={'username' : username, 'password' : password}
    )
    assert message in response.data
#End test register-------

#Test login-------
def test_login_succeed(auth, client, seed_user):
    assert client.get('/auth/login').status_code == 200

    response = auth.login()
    assert response.status_code == 302
    assert response.headers['Location'] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user.username == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('a', '', b'This user or password are incorrect. Try again'),
    ('', 'a', b'This user or password are incorrect. Try again'),
    ('a', 'a', b'This user or password are incorrect. Try again'),
))
def test_login_fail(auth, client, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

#End test login-------

#Test logout--------
def test_logout(auth, client, seed_user):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

#End test logout----





