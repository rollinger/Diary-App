import pytest

from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory

User = get_user_model()

@pytest.fixture
def user() -> User:
    return UserFactory()
