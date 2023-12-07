from iebank_api.models import Account, User, Transaction
import pytest

def test_create_admin_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, password, admin and created_at fields are defined correctly
    """
    user = User('Francisco Magot', 'francisco@magot.com', 'Peru', True)
    assert user.username == 'Francisco Magot'
    assert user.email == 'francisco@magot.com'
    assert user.password == 'Peru'
    assert user.admin == True

def test_create_nonadmin_user():
    """
    GIVEN a User model
    WHEN a new admin User is created
    THEN check the username, email, password, admin and created_at fields are defined correctly
    """
    admin_user = User("admin", "admin@test.com", "password", True)
    assert admin_user.username == 'admin'
    assert admin_user.email == 'admin@test.com'
    assert admin_user.password == 'password'
    assert admin_user.admin == True

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    user = User("John Doe", "john@doe.com" , "password")
    account = Account('John Doe', '€','India', user.id)
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.country == 'India'
    assert account.account_number != None
    assert account.balance == 1000.0
    assert account.status == 'Active'
    assert account.user_id == user.id

def test_make_transaction():
    """
    GIVEN a Transaction model
    WHEN a new Transaction is created
    THEN check the amount, currency, created_at, account_id and destination_account_id fields are defined correctly
    """
    user1 = User("John Doe", "john@doe.com", "password")
    user2 = User("Jane Doe", "jane@doe.com", "password")
    sender_account = Account('John Doe', '€', 'India', user1.id)
    receiver_account = Account('Jane Doe', '€', 'Spain', user2.id)
    transaction = Transaction(100.0, '€', sender_account.id, receiver_account.id)
    sender_account.balance -= transaction.amount
    receiver_account.balance += transaction.amount
    assert transaction.amount == 100.0
    assert transaction.currency == '€'
    assert transaction.account_id == sender_account.id
    assert transaction.destination_account_id == receiver_account.id
    assert sender_account.balance == 900.0
    assert receiver_account.balance == 1100.0
