import pytest
from datetime import timedelta
from time import sleep
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory
from factory import Faker
from journal.diary.models import Entry, Emotion

User = get_user_model()

@pytest.mark.django_db
def test_create_journal_entry():
    """ Make sure the entry get only saved if user and text is present.
    Test that the date is added if left blank and is equal to today
    """
    pass


@pytest.mark.django_db
def test_my_entries_method():
    """ Make sure the Entry.objects.my_entries() method returns only
    the user entries and is sorted descendingly.
    """
    pass


@pytest.mark.django_db
def test_new_user_has_normal_user_group():
    """ Make sure the a newly created user is member of the normal user group.
    See users.signals
    """
    pass