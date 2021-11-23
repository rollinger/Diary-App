from django.contrib.auth import get_user_model
from rest_framework import serializers

from timekeeping.models import Project, Task

from user.api.serializers import UserSerializer

User = get_user_model()


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
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
    project   = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:project-detail',
        lookup_field="slug"
    )
    status    = serializers.CharField(source='get_status_display')
    class Meta:
        model = Task
        fields = ["project", "title", "description", "status", "slug",]
        extra_kwargs = {
            "url": {"view_name": "api:task-detail", "lookup_field": "slug"}
        }