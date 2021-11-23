from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from timekeeping.models import Project

from .serializers import ProjectSerializer

User = get_user_model()


class ProjectViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = "slug"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(owner=self.request.user.id)
