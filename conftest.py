import pytest
from django.core.management import call_command
from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory

User = get_user_model()

# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'worklog/fixtures/dummy_data.json')

@pytest.fixture
def user() -> User:
    return UserFactory()