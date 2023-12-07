import pytest
from iebank_api.models import Account, User
from iebank_api import db, app


@pytest.fixture
def testing_client(scope='module'):
    with app.app_context():
        db.create_all()
        admin_user = User("admin_test", "admin@admin.com", "admin", True)
        nonadmin_user = User("user_test", "user@test.com", "user", False)
        db.session.add_all([admin_user, nonadmin_user])
        db.session.commit()
        account1 = Account('Test Account 1', '€', 'Spain', nonadmin_user.id)
        account2 = Account('Test Account 2', '€', 'Spain', admin_user.id)
        db.session.add_all([account1, account2])
        db.session.commit()

        with app.test_client() as testing_client:
            yield testing_client

        db.drop_all()