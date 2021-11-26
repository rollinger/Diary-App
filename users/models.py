from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
	""" User Model for extending functionalities

	url: /api/users/<username>
	"""
	class Meta:
		ordering = ("username",)