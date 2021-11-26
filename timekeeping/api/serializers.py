import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import serializers

from timekeeping.models import TaskAssignment, Project, Task

from users.api.serializers import UserSerializer

User = get_user_model()


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
	""" Serializer for a Project of an Owner
	url links to owner 
	list of tasks as urls
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
		#queryset=TaskAssignment.objects.all(),
		view_name='api:taskassignment-detail',
		lookup_field="id"
	)

	class Meta:
		model = Task
		fields = ["url", "project", "title", "description", "status", "assignments"]
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
	allowed = serializers.BooleanField(
		default=True
	)
	max_workload = serializers.DurationField(
		default = datetime.timedelta(0)
	)
	class Meta:
		model = TaskAssignment
		fields = ["user", "task", "max_workload", "current_workload", "allowed", "current_log", "archived_log"]
		extra_kwargs = {
			"url": {"view_name": "api:taskassignment-detail", "lookup_field": "id"}
		}
