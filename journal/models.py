import uuid
from datetime import date
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

	created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated at"), auto_now=True)


class Emotion(BaseModel):
	""" Emotion Model
	Defines an Emotion associated to a Journal entry.
	
	name: emotion name
	"""

	class Meta:
		verbose_name = _("Emotion")
		verbose_name_plural = _("Emotions")
		ordering = ("name",)
	
	name  = models.CharField(
        _("Name"),
        help_text=_("Name of the Emotion"),
        max_length=255, unique=True
    )

	def __str__(self):
		return _("%s") % (self.name)


class EntryManager(models.Manager):
	""" Manager for Entries

	my_entries(user): returns a list of entries descendingly sorted
	"""
	
	def my_entries(self, user):
		""" Returns a list of entries descendingly sorted."""
		return self.filter(user=user).order_by("-occasion")


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
		ordering = ("-occasion",)

	user = models.ForeignKey(
        User,
        help_text=_("Author of the entry"),
        related_name="entries",
        blank=True, on_delete=models.CASCADE,
    )

	occasion = models.DateField(
		_("Occasion"), 
		help_text=_("Date the entry was made"),
		blank=True,
	)

	text = models.TextField(
        _("Entry Text"),
        help_text=_("The journal text"),
        max_length=5000,
    )

	emotions = models.ManyToManyField(
		Emotion,
        help_text=_("The journal text"),
		blank=True,
	)

	objects = EntryManager()

	def __str__(self):
		return _("%s Entry from %s") % (self.user, self.occasion)

	def save(self, *args, **kwargs):
		if not self.occasion:
			self.occasion = date.today() #FIX: timezone aware...!
		super(Entry, self).save(*args, **kwargs)