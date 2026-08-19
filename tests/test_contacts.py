import pytest

from conelman.models import Contact
from conelman.db import get_db
from sqlalchemy import select

#Index tests--------
def test_index_without_login(client):
    response = client.get("/")

    #Connection to index page
    assert response.status_code == 200

    #Menu and index messages
    assert b'Log in' in response.data
    assert b'Sign up' in response.data
    assert b'Log out' not in response.data
    assert b'Add contact' not in response.data

def test_index_with_login_and_without_contact(auth, client, seed_user):
    auth.login()
    response = client.get("/")

    #Connection to index page
    assert response.status_code == 200

    #Menu and index messages
    assert b'Log out' in response.data
    assert b'Add contact' in response.data
    assert b'Log in' not in response.data
    assert b'Sign up' not in response.data
    assert b"Contact manager for all!" not in response.data
    assert b'Edit' not in response.data
    assert b'Delete' not in response.data
    

def test_index_with_login_and_with_contacts(auth, client, seed_user, seed_contacts):
    auth.login()
    response = client.get("/")
    contact_illojuan = b"illojuan"

    #Contact add to test user
    assert b'illojuan' in response.data
    assert b'928247364' in response.data
    assert b'streamer' in response.data

    #Contact actions
    assert b'Edit' in response.data
    assert b'Delete' in response.data

    #Menu and index messages
    assert b'Add contact' in response.data
    assert b'Log out' in response.data
    assert b"Contact manager for all!" not in response.data
    assert b'Log in' not in response.data
    assert b'Sign up' not in response.data
#End index tests-----

#Add contact tests-------
def test_add_contact_page(auth, client, seed_user):
    auth.login()
    response = client.get('/contact/add')

    #Connection to add contact page
    assert response.status_code == 200

    #Form messages
    assert b'Name' in response.data
    assert b'Phone' in response.data
    assert b'Notes' in response.data
    assert b'Save' in response.data

@pytest.mark.parametrize(('name', 'phone', 'notes'),(
    ('pepe', '928483745', 'amigo'),
    ('papa', '928483746', ''),
))
def test_add_contact_succeed(auth, client, seed_user, app, name, phone, notes):
    auth.login()
    response = client.post(
        '/contact/add', data = {'name' : name, 'phone' : phone, 'notes' : notes}
    )

    #Redirect to index
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    #Added contact sucessfully
    with app.app_context():
        assert get_db().session.scalars(
            select(Contact).where(
                Contact.name == name, 
                Contact.phone == phone, 
                Contact.notes == notes
            )
        ).first() is not None

@pytest.mark.parametrize(('name', 'phone', 'notes', 'message'),(
    ('test', 'a', 'test', b'Invalid number.'),
    ('test', '92847', 'test', b'Invalid number.'),
    ('test', '', 'test', b'Invalid number.'),
    ('', '928474589', 'test', b'Empty name.'),
))
def test_add_contact_fail(auth, client, seed_user, name, phone, notes, message):
    auth.login()
    response = client.post(
        '/contact/add' , data = {'name' : name, 'phone' : phone, 'notes' : notes}
    )

    assert message in response.data
#End contact tests-------






    