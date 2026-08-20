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

@pytest.mark.parametrize('contacts_to_test', [
    pytest.param(
        {
        'name' : 'pepe', 
        'phone' : '928483745', 
        'notes' : 'amigo'
        }, 
        id = "contact_with_notes"
    ),
    pytest.param(
        {
        'name' : 'papa', 
        'phone' : '928483746', 
        'notes' : ''
        }, 
        id = "contact_without_notes"
    ),
    pytest.param(
        {
        'name' : 'papaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 
        'phone' : '928483746', 
        'notes' : ''
        }, 
        id = "contact_with_long_name"
    ),
])

def test_add_contact_succeed(auth, client, seed_user, app, contacts_to_test):
    auth.login()
    response = client.post(
        '/contact/add', data = {
            'name' : contacts_to_test['name'], 
            'phone' : contacts_to_test['phone'], 
            'notes' : contacts_to_test['notes']
        }
    )

    #Redirect to index
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

    #Added contact sucessfully
    with app.app_context():
        assert get_db().session.scalars(
            select(Contact).where(
                Contact.name == contacts_to_test['name'], 
                Contact.phone == contacts_to_test['phone'], 
                Contact.notes == contacts_to_test['notes']
            )
        ).first() is not None


@pytest.mark.parametrize('contacts_to_test', [
    pytest.param(
        {
            'name': 'test',
            'phone': 'a',       
            'notes': 'test',
            'message': b'Invalid number.'
        },
        id='phone_non_numeric'
    ),
    pytest.param(
        {
            'name': 'test',
            'phone': '92847',
            'notes': 'test',
            'message': b'Invalid number.'
        },
        id='phone_too_short'
    ),
    pytest.param(
        {
            'name': 'test', 
            'phone': '',       
            'notes': 'test',
            'message': b'Invalid number.'
        },
        id='phone_empty'
    ),
    pytest.param(
        {
            'name': '',     
            'phone': '928474589', 
            'notes': 'test',
            'message': b'Empty name.'
        },
        id='name_empty'
    ),
    pytest.param(
        {
            'name': 'a',
            'phone': '9284863488',
            'notes': '',
            'message': b'Invalid number.',
        },
        id='phone_too_long',
    ),
])
def test_add_contact_fail(auth, client, seed_user, contacts_to_test):
    auth.login()
    response = client.post(
        '/contact/add' , 
        data = 
        {
            'name' : contacts_to_test['name'], 
            'phone' : contacts_to_test['phone'], 
            'notes' : contacts_to_test['notes']
        }
    )

    assert contacts_to_test['message'] in response.data
#End add contact tests--------

#Edit contact test------
def test_edit_contact_succeed(auth, client, app, seed_user, seed_contacts):
    auth.login()
    #Test if edit page works
    assert client.get("/contact/1/edit").status_code == 200

    #Test if changing contact works
    response = client.post(
        '/contact/1/edit', data = {
            'name' : 'illojuanYT', 'phone' : '928438799', 'notes' : 'streamer and youtuber'
        }
    )
    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    #Confirm change of contact
    with app.app_context():
        assert get_db().session.scalars(
            select(Contact).where(
                Contact.name == "illojuanYT",
                Contact.phone == "928438799",
                Contact.notes == "streamer and youtuber"
            )
        ) is not None


@pytest.mark.parametrize('contacts_edits_test', [
    pytest.param(
        {
            'name': '',
            'phone': '',
            'notes': '',
            'message': b'Invalid name.',
        },
        id='name_empty_and_phone_empty',
    ),
    pytest.param(
        {
            'name': 'a',
            'phone': '',
            'notes': '',
            'message': b'Invalid number.',
        },
        id='phone_empty',
    ),
    pytest.param(
        {
            'name': 'a',
            'phone': '9',
            'notes': '',
            'message': b'Invalid number.',
        },
        id='phone_too_short',
    ),
    pytest.param(
        {
            'name': 'a',
            'phone': 'a',
            'notes': '',
            'message': b'Invalid number.',
        },
        id='phone_non_numeric',
    ),
    pytest.param(
        {
            'name': 'a',
            'phone': '92848634',
            'notes': '',
            'message': b'Invalid number.',
        },
        id='phone_not_enough_length',
    ),
    pytest.param(
        {
            'name': 'a',
            'phone': '9284863456',
            'notes': '',
            'message': b'Invalid number.',
        },
        id='phone_too_long',
    ),
])
def test_edit_contact_with_errors(auth, client, seed_user, seed_contacts, contacts_edits_test):
    auth.login()
    response = client.post(
        '/contact/1/edit',
        data = {
            'name' : contacts_edits_test['name'],
            'phone' : contacts_edits_test['phone'],
            'notes' : contacts_edits_test['notes']
        }
    )

    assert contacts_edits_test['message'] in response.data
#End edit contact tests-------

#Delete contact tests-----
def test_delete_contact(auth, client, app, seed_user, seed_contacts):
    auth.login()
    response = client.get('/contact/1/delete')

    assert response.status_code == 302
    assert response.headers["Location"] == '/'

    with app.app_context():
        assert get_db().session.scalars(
            select(Contact).where(
                Contact.name == 'illojuan',
                Contact.phone == '928247364',
                Contact.notes == 'streamer'
            )
        ).first() is None
#End delete contact tests-----






    