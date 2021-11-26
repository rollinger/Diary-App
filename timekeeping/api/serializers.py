import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers

from timekeeping.models import TaskAssignment, Project, Task, Worklog

from users.api.serializers import UserSerializer

User = get_user_model()


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
	""" Serializer for a Project
	"""
	owner = serializers.HyperlinkedRelatedField(
	    many=False,
	    read_only=False,
		queryset=User.objects.all(),
	    view_name='api:user-detail',
	    lookup_field="username"
	)

	tasks = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='api:task-detail',
		lookup_field="slug"
	)

	class Meta:
		model = Project
		fields = ["url", "owner", "title", "description", "tasks"]
		extra_kwargs = {
			"url": {"view_name": "api:project-detail", "lookup_field": "slug"}
		}


class TaskSerializer(serializers.HyperlinkedModelSerializer):
	""" Serializer for a Task
	"""
	project   = serializers.HyperlinkedRelatedField(
		many=False,
		read_only=False,
		queryset=Project.objects.all(),
		view_name='api:project-detail',
		lookup_field="slug"
	)
	assignments = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		# queryset=TaskAssignment.objects.all(),
		view_name='api:assignment-detail',
		lookup_field="id"
	)

	class Meta:
		model = Task
		fields = ["project", "title", "description", "status", "assignments"]
		extra_kwargs = {
			"url": {"view_name": "api:task-detail", "lookup_field": "slug"}
		}


class TaskAssignmentSerializer(serializers.HyperlinkedModelSerializer):
	task = serializers.HyperlinkedRelatedField(
		many=False,
		read_only=False,
		queryset=Task.objects.all(),
		view_name='api:task-detail',
		lookup_field="slug"
	)
	user = serializers.HyperlinkedRelatedField(
		many=False,
		read_only=False,
		queryset=User.objects.all(),
		view_name='api:user-detail',
		lookup_field="username"
	)
	worklogs = serializers.HyperlinkedRelatedField(
		many=True,
		read_only=True,
		view_name='api:worklog-detail',
		lookup_field="id"
	)
	allowed = serializers.BooleanField(
		default=True
	)
	max_workload = serializers.DurationField(
		default = datetime.timedelta(0)
	)
	class Meta:
		model = TaskAssignment
		fields = ["user", "task", "max_workload", "allowed", "worklogs"]
		extra_kwargs = {
			"url": {"view_name": "api:assignment-detail", "lookup_field": "id"}
		}


class WorklogSerializer(serializers.HyperlinkedModelSerializer):
	assignment = serializers.HyperlinkedRelatedField(
		many=False,
		read_only=False,
		queryset=TaskAssignment.objects.all(),
		view_name='api:assignment-detail',
		lookup_field="id"
	)
	time = serializers.DurationField(
		label=_("Manual Time"),
		default = datetime.timedelta(0)
	)
	class Meta:
		model = Worklog
		fields = ["assignment", "start", "stop", "time", "notes"]
		extra_kwargs = {
			"url": {"view_name": "api:worklog-detail", "lookup_field": "id"}
		}