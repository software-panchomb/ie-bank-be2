from iebank_api import app
import pytest

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€','country': 'India'})
    assert response.status_code == 200

# Is the following correct?

# Since There is a fake guy called John Doe, i'll go ahead with the following.
def test_get_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a single account page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts/1')  
    assert response.status_code == 200

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>' page is put to (PUT)
    THEN check the response is valid
    """
    response = testing_client.put('/accounts/1', json={'name': 'Updated Name'}) 
    assert response.status_code == 200

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<int:id>' page is deleted (DELETE)
    THEN check the response is valid
    """
    response = testing_client.delete('/accounts/1')  
    assert response.status_code == 200