import pytest
from rest_framework.authtoken.models import Token
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db

def test_user_has_auth_token(user: User):
    assert(user.auth_token != None)
    assert(type(user.auth_token) == Token)


def test_user_detail(user: User):
    assert (
        reverse("api:user-detail", kwargs={"username": user.username})
        == f"/api/users/{user.username}/"
    )
    assert resolve(f"/api/users/{user.username}/").view_name == "api:user-detail"


def test_user_list():
    assert reverse("api:user-list") == "/api/users/"
    assert resolve("/api/users/").view_name == "api:user-list"


# def test_user_me():
#     assert reverse("api:user-me") == "/api/users/me/"
#     assert resolve("/api/users/me/").view_name == "api:user-me"