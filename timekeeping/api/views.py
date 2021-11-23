from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet,GenericViewSet

from timekeeping.models import Project, Task

from .serializers import ProjectSerializer, TaskSerializer

User = get_user_model()


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self, *args, **kwargs):
    #     return self.queryset.filter(owner=self.request.user.id)

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticated]