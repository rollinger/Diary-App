from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from timekeeping.models import Project, Task, TaskAssignment, Worklog

from .serializers import ProjectSerializer, TaskSerializer, TaskAssignmentSerializer, WorklogSerializer

User = get_user_model()

#
# Generic Viewsets with CRUD interfaces for Admin Users (is_staff and more)
#

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]


class TaskAssignmentViewSet(ModelViewSet):
    serializer_class = TaskAssignmentSerializer
    queryset = TaskAssignment.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAdminUser]


class WorklogViewSet(ModelViewSet):
    serializer_class = WorklogSerializer
    queryset = Worklog.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAdminUser]

    # @action(methods=['put'], detail=True, permission_classes=[IsAuthenticated])
    # def add_worklog(self, request, pk=None):
    #     pass

#
# Specific Views for Authenticated Users who do the time logging (worker)
#

class TaskAssignmentWorkerViewSet(ModelViewSet):
    serializer_class = TaskAssignmentSerializer
    queryset = TaskAssignment.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(user=self.request.user)

class WorklogWorkerViewSet(ModelViewSet):
    serializer_class = WorklogSerializer
    queryset = Worklog.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(assignment__user=self.request.user)