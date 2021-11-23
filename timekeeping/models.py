import uuid

from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class BaseModel(models.Model):
	"""
	Defines the abstract timestamps, uuid and slug for Timekeeping models
	"""

	class Meta:
		abstract = True

	id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, 
		editable=False, unique=True, name='id'
	)
	created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated at"), auto_now=True)



class Project(BaseModel):
	""" Project Model
	"""

	class Meta:
		verbose_name = _("Project")
		verbose_name_plural = _("Projects")

	owner = models.ForeignKey(
        User,
        help_text=_("Owned by user"),
        null=True,
        blank=True,
        related_name="owned_projects",
        on_delete=models.CASCADE,
    )
	title = models.CharField(
        _("Title"),
        help_text=_("Title of the Project"),
        max_length=255,
    )
	slug = models.SlugField(
        _("Unique Slug Identifier"), 
		max_length=255, 
		allow_unicode=True, unique=True
    )
	description = models.TextField(
        _("Description"),
        help_text=_("Description of the Project"),
        max_length=2000,
        blank=True,
    )

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Project, self).save(*args, **kwargs)


TASK_STATE_CHOICE = (
	("planned",_("Task is planned")),
	("started",_("Task is started")),
	("hold",_("Task is on hold")),
	("finished",_("Task is finished")),
)

class Task(BaseModel):
	""" Task Model
	"""

	class Meta:
		verbose_name = _("Task")
		verbose_name_plural = _("Tasks")

	project = models.ForeignKey(
        Project,
        help_text=_("Task belongs to project"),
        null=True,
        blank=True,
        related_name="tasks",
        on_delete=models.CASCADE,
    )

	title = models.CharField(
        _("Title"),
        help_text=_("Title of the Task"),
        max_length=255,
    )

	slug = models.SlugField(
        _("Unique Slug Identifier"), 
		max_length=255, 
		allow_unicode=True, unique=True
    )

	description = models.TextField(
        _("Description"),
        help_text=_("Description of the Task"),
        max_length=2000,
        blank=True,
    )

	status = models.CharField(
        _("State"),
        help_text=_("State of the task"),
        max_length=100,
        choices=TASK_STATE_CHOICE,
        default="planned",
    )

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Task, self).save(*args, **kwargs)