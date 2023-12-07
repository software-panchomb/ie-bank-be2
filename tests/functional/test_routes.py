from iebank_api import app
from conftest import admin_username, nonadmin_username
import pytest
import pdb

def test_admin_login(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/login', json={'email': f'{admin_username}@test.com', 'password': 'test'})
    assert response.status_code == 200
    assert response.json['is_admin'] == True

def test_nonadmin_login(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/login', json={'email': f'{nonadmin_username}@test.com', 'password': 'test'})
    assert response.status_code == 200
    assert response.json['is_admin'] == False

def test_admin_get_accounts(testing_client, admin_session):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts', headers={'Cookie': admin_session})
    assert response.status_code == 200
    assert len(response.json['accounts']) == 2

def test_nonadmin_get_accounts(testing_client, nonadmin_session):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts', headers={'Cookie': nonadmin_session})
    assert response.status_code == 200
    assert len(response.json['accounts']) == 1

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client, admin_session):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'}, headers={'Cookie': admin_session})
    assert response.status_code == 200

# def test_update_account(testing_client):
#     """
#     GIVEN a Flask application
#     WHEN the '/accounts' page is posted to (PUT)
#     THEN check the response is valid
#     """
#     response = testing_client.put('/accounts/1', json={'name': 'John Doe', 'country': 'Spain'})
#     assert response.status_code == 200

# def test_get_account(testing_client):
#     """
#     GIVEN a Flask application
#     WHEN the '/accounts' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = testing_client.get('/accounts/1')
#     assert response.status_code == 200

# def test_delete_account(testing_client):
#     """
#     GIVEN a Flask application
#     WHEN the '/accounts' page is posted to (DELETE)
#     THEN check the response is valid
#     """
#     response = testing_client.delete('/accounts/1')
#     assert response.status_code == 200


def test_admin_logout(testing_client, admin_session):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/logout', headers={'Cookie': admin_session})
    assert response.status_code == 200

def test_nonadmin_logout(testing_client, admin_session, nonadmin_session):
    """
    GIVEN a Flask application
    WHEN the '/logout' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/logout', headers={'Cookie': nonadmin_session})
    #pdb.set_trace()
    assert response.status_code == 200


# def test_root(testing_client):
#     """
#     GIVEN a Flask application
#     WHEN the '/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = testing_client.get('/')
#     assert response.status_code == 200

# def test_skull(testing_client):
#     """
#     GIVEN a Flask application
#     WHEN the '/skull' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = testing_client.get('/skull')
#     assert response.status_code == 200