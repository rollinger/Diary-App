from typing import Any, Sequence
import pytest
from django.contrib.auth import get_user_model
from factory import Faker
from factory.django import DjangoModelFactory
from users.tests.factories import UserFactory
from timekeeping.models import Project, Task, TaskAssignment

pytestmark = pytest.mark.django_db

class ProjectFactory(DjangoModelFactory):
    """ Factory for faking Project instances """
    owner = UserFactory()
    title = Faker("title")
    description = Faker("description")

    class Meta:
        model = Project
        django_get_or_create = ["slug"]

class TaskFactory(DjangoModelFactory):
    """ Factory for faking Task instances """
    # username = Faker("user_name")
    # email = Faker("email")
    # username = Faker("user_name")
    # email = Faker("email")
    class Meta:
        model = Task
        django_get_or_create = ["slug"]

class TaskAssignmentFactory(DjangoModelFactory):
    """ Factory for faking TaskAssignment instances """
    # username = Faker("user_name")
    # email = Faker("email")
    # username = Faker("user_name")
    # email = Faker("email")
    class Meta:
        model = TaskAssignment
        django_get_or_create = ["id"]

