from enum import unique
import uuid

from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


User = get_user_model()


TASK_STATE_CHOICE = (
	# Task lifecycle. Only started can be logged. Default is started
	("planned",_("Task is planned")),
	("started",_("Task is started")),
	("hold",_("Task is on hold")),
	("finished",_("Task is finished")),
)


class BaseModel(models.Model):
	"""
	Defines the abstract timestamps and unique id for subsequent timekeeping models
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
	Defines a project that has a number of tasks on which to work on.
	
	owner: project manager
	slug: on_save via title

	url: /api/projects/<slug>
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



class Task(BaseModel):
	""" Task Model
	A task of a project. Has task assignments <m2m> User that can log time on.
		
	project: parent project
	slug: on_save via title
	status: task lifecycle. started allows logging


	url: /api/projects/<project_slug>/tasks/<task_slug>
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
        default="started",
    )

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super(Task, self).save(*args, **kwargs)


class TaskAssignment(BaseModel):
	""" Assignment Model
	A User is assigned to a task of a project and can log work time.
		
	task: parent task
	user: assigned to work on task
	allowed: logging allowed switch
	max_workload: maximum workload allowed for the assignment


	url: /api/projects/<project_slug>/tasks/<task_slug>/assignment/<uuid>
	"""

	class Meta:
		verbose_name = _("Task Assignment")
		verbose_name_plural = _("Task Assignments")
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

	allowed = models.BooleanField(
		_("Allowed"),
		help_text = _("Logging Work is allowed"), 
		default=True
	)

	max_workload = models.DurationField(
		_("Maximum Workload"),
		help_text = _('Max workload in time. If left zero no workload cap.'), 
		default=0
	)

	current_workload = models.DurationField(
		_("Current Workload"),
		help_text = _('Work currently logged on this assignment'), 
		default=0
	)

	def can_start_log_time(self):
		"""Checks if all conditions are met to start logging time.
		- Task is started
		- Assignment is allowed
		- current workload < max workload
		"""
		pass

	def start_log_time(self):
		"""Starts a new worklog:
		Creates a new worklog and set start to now
		"""
		pass

	def end_log_time(self):
		"""Ends a worklog"""
		pass

	def __str__(self):
		return _("%s working on \"%s\"") % (self.user, self.task)

	def save(self, *args, **kwargs):
		super(TaskAssignment, self).save(*args, **kwargs)


class Worklog(BaseModel):
	""" Work Logging Model
	A User logs work for an assignment. The work was start

	assignment: associated to an assignment
	start: work start datetime
	stop: work end datetime
	time: duration of the work / manual time

	notes: worker notes or work references

	url: /api/projects/<project_slug>/tasks/<task_slug>/assignment/<uuid>/log/<user>/<uuid>
	"""

	class Meta:
		verbose_name = _("Worklog")
		verbose_name_plural = _("Worklog")
		ordering = ("start", "stop", "time")
		# TODO: Disallow logging for same assignment at the same timeframe...
		unique_together = ("assignment", "created_at") 

	assignment = models.ForeignKey(
        TaskAssignment,
        help_text=_("Worklog for assignments"),
        related_name="worklogs",
        on_delete=models.CASCADE,
    )

	completed = models.BooleanField(
		_("Completed"),
		help_text = _("The worklog instance is completed."), 
		default=False
	)

	start = models.DateTimeField(
		_('Started at'), help_text=_("Datetime when the work was started"), 
		null=True, blank=True
	)

	stop = models.DateTimeField(
		_('Ended on'), help_text=_("Datetime when the work was stopped"), 
		null=True, blank=True
	)

	time = models.DurationField(
		_('Manual Time'), help_text=_("Log manual time"), 
		null=True, blank=True
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

	@property
	def manual_time(self):
		if self.time and not self.start or not self.stop:
			return True
		return False

	def __str__(self):
		return _("%s (%s)") % (self.assignment, self.time)

	def save(self, *args, **kwargs):
		if self.completed == True and self.time == None:
			# Calculate time by start and stop if no manual time was given.
			self.time = self.stop - self.start
		super(Worklog, self).save(*args, **kwargs)
