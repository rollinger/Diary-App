import datetime
# from enum import unique
import uuid
import json
import pytz
from dateutil import parser
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

LOG_DEFAULT_JSON = {
    "start": None,
    "stop": None,
    "time": None,
    "notes": "",
	"completed": False}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code
	Use like json.dumps(datetime.now(), default=json_serial)
	"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def json_to_datetime(datetime_string):
    return pytz.timezone("Europe/Berlin").localize(parser.parse(datetime_string))


def get_current_log_default_json():
	return LOG_DEFAULT_JSON

def get_archive_log_list_json():
	return []

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


	url: /api/tasks/<slug>
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


	url: /api/assignment/<uuid>
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
		help_text = _('Max workload in time. If left zero no workload cap. Format: hh:mm:ss'), 
		default=datetime.timedelta()
	)

	current_workload = models.DurationField(
		_("Current Workload"),
		help_text = _('Work currently logged on this assignment. Format: hh:mm:ss'), 
		default=datetime.timedelta()
	)

	current_log = models.JSONField(
		_("Current Log"), help_text=_(""), 
		default=get_current_log_default_json
	)

	archived_log = models.JSONField(
		_("Archived Logs"), help_text=_(""), 
		default=get_archive_log_list_json
	)

	def __str__(self):
		return _("%s working on \"%s\"") % (self.user, self.task)

	def can_log_time(self, user):
		"""Checks if all conditions are met to start logging time.
		- Task is started
		- Assignment is allowed
		- current workload < max workload
		"""
		if (self.user == user and
			self.task.status == 'started' and
			self.allowed and
			self.current_workload < self.max_workload):
			return True
		return False

	def start_log_time(self, user, notes=None):
		""" Starts a new worklog:
		Creates a new worklog and set start to now, 
		appends notes if passed.
		"""
		if self.can_log_time(user):
			self.current_log = get_current_log_default_json()
			self.current_log['start'] = json_serial(datetime.datetime.now())
			if notes:
				self.current_log['notes'] = notes
			self.save()
			return True
		return False

	def stop_log_time(self, user, notes=None):
		""" Stops a worklog: 
		Logs stop time, calcs the duration and sets to completed
		"""
		if self.can_log_time(user) and self.current_log['completed'] == False:
			self.current_log['stop'] = json_serial(datetime.datetime.now())
			time = json_to_datetime(self.current_log['stop']) - json_to_datetime(self.current_log['start'])
			self.current_log['time'] = time.total_seconds()
			if notes:
				self.current_log['notes'] += "\n" + notes
			self.current_log['completed'] = True
			self.archived_log.append( self.current_log )
			self.save()
			return True
		return False

	def save(self, *args, **kwargs):
		""" On save calculates the total seconds logged as the current workload."""
		seconds = 0
		for log in self.archived_log:
			seconds += log["time"]
		self.current_workload = datetime.timedelta(seconds=seconds)
		super(TaskAssignment, self).save(*args, **kwargs)

"""
Print("Starting Log:")
phil = User.objects.get(username="philipp")
ta = TaskAssignment.objects.all().first()
ta.can_log_time(phil)
ta.start_log_time(phil,notes="Start Test")
print(ta.current_log)

Print("Stopping Log:")
phil = User.objects.get(username="philipp")
ta = TaskAssignment.objects.all().first()
ta.can_log_time(phil)
ta.stop_log_time(phil,notes="Stop Test")
print(ta.current_log)
"""