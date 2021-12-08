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


class Entry(BaseModel):
	""" Entry Model
	Defines an Journal entry. A text at a date from a user
	
	user: who made the entry
	date: when the entry was made
	text: the entry
	emotions: emotion tags
	"""

	class Meta:
		verbose_name = _("Entry")
		verbose_name_plural = _("Entries")
		ordering = ("-date",)
		unique_together = ("user", "date")

	user = models.ForeignKey(
        User,
        help_text=_("Author of the entry"),
        null=True,
        blank=True,
        related_name="entries",
        on_delete=models.CASCADE,
    )

	date = models.DateField(
		_("Date"), 
		help_text=_("Date the entry was made"),
		auto_now_add=True
	)

	text = models.TextField(
        _("Entry Text"),
        help_text=_("The journal text"),
        max_length=5000,
    )

	def __str__(self):
		return _("%s Entry from %s") % (self.user, self.date)

	def save(self, *args, **kwargs):
		super(Entry, self).save(*args, **kwargs)