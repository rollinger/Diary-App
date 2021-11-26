from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from timekeeping.models import Project, Task, Assignment, Worklog

from .serializers import ProjectSerializer, TaskSerializer, AssignmentSerializer, WorklogSerializer

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


class AssignmentViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
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

class AssignmentWorkerViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
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