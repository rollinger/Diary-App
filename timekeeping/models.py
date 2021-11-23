import uuid

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

	unique_id = models.UUIDField(
		default=uuid.uuid4, 
		editable=False, unique=True
	)
	slug = models.SlugField(
        _("Unique Slug Identifier"), 
		max_length=255, allow_unicode=True, unique=True
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
        blank=True,
    )
	description = models.CharField(
        _("Description"),
        help_text=_("Description of the Project"),
        max_length=2000,
        blank=True,
    )


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
        blank=True,
    )

	description = models.CharField(
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