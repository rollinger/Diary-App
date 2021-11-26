from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

class User(AbstractUser):
	""" User Model for extending functionalities
	"""
	class Meta:
		ordering = ("username",)