from django.contrib.auth import get_user_model
from rest_framework import serializers

from timekeeping.models import Project

from user.api.serializers import UserSerializer

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    owner   = UserSerializer()
    class Meta:
        model = Project
        fields = "__all__"
        # fields = [
        #     "__all__",
        # ]

        # extra_kwargs = {
        #     "url": {"view_name": "api:project-detail", "lookup_field": "slug"}
        # }
