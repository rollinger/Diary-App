from enum import unique
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
		ordering = ("title",)
		unique_together = ("owner", "title")

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
		ordering = ("project", "title")
		unique_together = ("project", "title")

	project = models.ForeignKey(
        Project,
        help_text=_("Task belongs to project"),
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
			self.slug = slugify(self.project, self.title)
		super(Task, self).save(*args, **kwargs)


class Assignment(BaseModel):
	""" Assignment Model
	A User is assigned to a task of a project and can log work under the projects
	"""

	class Meta:
		verbose_name = _("Assignment")
		verbose_name_plural = _("Assignments")
		ordering = ("task", "user")
		unique_together = ("user", "task")
	
	task = models.ForeignKey(
        Task,
        help_text=_("Task of assignment"),
        related_name="assignments",
        on_delete=models.CASCADE,
    )
	
	user = models.ForeignKey(
        User,
        help_text=_("User of assignment"),
        related_name="assignments",
        on_delete=models.CASCADE,
    )

	slug = models.SlugField(
        _("Unique Slug Identifier"), 
		max_length=255, 
		allow_unicode=True, unique=True
    )

	allowed = models.BooleanField(
		_("Allowed"),
		help_text = _("Logging Work is allowed"), 
		default=True
	)

	max_workload = models.DurationField(
		_("Maximum Workload"),
		help_text = _('Max workload in hours. If left zero no workload cap.'), 
		default=0
	)

	def __str__(self):
		return _("%s working on \"%s\"") % (self.user, self.task)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user, self.task)
		super(Assignment, self).save(*args, **kwargs)


class Worklog(BaseModel):
	""" Work log Model
	A User logs work for an assignment. The work was start
	"""

	class Meta:
		verbose_name = _("Worklog")
		verbose_name_plural = _("Worklog")
		ordering = ("start", "stop", "time")
		# TODO: Disallow logging for same assignment at the same timeframe
		unique_together = ("assignment", "created_at") 

	assignment = models.ForeignKey(
        Assignment,
        help_text=_("Worklog for assignments"),
        related_name="worklogs",
        on_delete=models.CASCADE,
    )

	slug = models.SlugField(
        _("Unique Slug Identifier"), 
		max_length=255, 
		allow_unicode=True, unique=True
    )

	start = models.DateTimeField(
		_('Started at'), help_text=_("Datetime when the work was started"), null=True, blank=True
	)

	stop = models.DateTimeField(
		_('Ended on'), help_text=_("Datetime when the work was stopped"), null=True, blank=True
	)

	time = models.DurationField(
		_('Manual Time'), help_text=_("Log manual time"), null=True, blank=True
	)

	notes = models.TextField(
        _("Notes"),
        help_text=_("Notes / References for the log"),
        max_length=2000,
        blank=True,
    )

	@property
	def workload(self):
		return self.time

	def __str__(self):
		return _("%s for %s") % (self.assignment, self.time)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.assignment, self.created_at)
		super(Worklog, self).save(*args, **kwargs)
