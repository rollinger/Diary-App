import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseModel(models.Model):
	"""
	Defines the abstract timestamps and unique id for subsequent diary models
	"""

	class Meta:
		abstract = True

	id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, 
		editable=False, unique=True, name='id'
	)
	created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated at"), auto_now=True)