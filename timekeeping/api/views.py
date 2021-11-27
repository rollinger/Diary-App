from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from timekeeping.models import Project, Task, TaskAssignment

from .serializers import (
    ProjectSerializer, 
    TaskSerializer, 
    TaskAssignmentSerializer, 
    #NoteSerializer,
)

User = get_user_model()

#
# Generic Viewsets with CRUD interfaces for Admin Users (is_staff and more)
#

class ProjectViewSet(ModelViewSet):
    """ Generic Project ModelViewSet

    CRUD for for Staff User:
    /api/projects/	                timekeeping.api.views.ProjectViewSet	api:project-list
    /api/projects/<slug>/	        timekeeping.api.views.ProjectViewSet	api:project-detail
    
    ID via slug
    .<format>/	Suffix to specify response format.
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]

class TaskViewSet(ModelViewSet):
    """ Generic Task ModelViewSet

    CRUD for for Staff User: 
    /api/tasks/	        timekeeping.api.views.TaskViewSet	api:task-list
    /api/tasks/<slug>/	timekeeping.api.views.TaskViewSet	api:task-detail

    ID via slug
    .<format>/	Suffix to specify response format.
    """
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    lookup_field = "slug"
    permission_classes = [permissions.IsAdminUser]


class TaskAssignmentViewSet(ModelViewSet):
    """ Generic Task Assignment ModelViewSet

    CRUD for for Staff User:
    /api/taskassignments/	    timekeeping.api.views.TaskAssignmentViewSet	api:taskassignment-list
    /api/taskassignments/<id>/	timekeeping.api.views.TaskAssignmentViewSet	api:taskassignment-detail

    START/STOP for workers
    /api/taskassignments/<id>/start_worklog/	timekeeping.api.views.TaskAssignmentViewSet	api:taskassignment-start-worklog
    /api/taskassignments/<id>/stop_worklog/	    timekeeping.api.views.TaskAssignmentViewSet	api:taskassignment-stop-worklog
    
    ID via UUID <id>
    .<format>/	Suffix to specify response format.
    """
    serializer_class = TaskAssignmentSerializer
    queryset = TaskAssignment.objects.all()
    lookup_field = "id"
    permission_classes = [permissions.IsAdminUser]

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def start_worklog(self, request, pk=None):
        """ Authenticated Users can START a worklog on their assignment 
        The timestamp is set on the backend. Optional pass a note (TODO: Not implemented yet).
        Permissions (can_log_time) is checked on the model.
        """
        assignment = self.get_object()
        user = self.request.user
        if assignment.start_log_time(user, notes=None):
            return Response(TaskAssignmentSerializer(assignment).data)
        return Response({'Can not start log': 'Assignment not open for logging.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def stop_worklog(self, request, pk=None):
        """ Authenticated Users can STOP a worklog on their assignment 
        The timestamp is set on the backend. Optional leave a note (TODO: Not implemented yet).
        Permissions (can_log_time) is checked on the model.
        """
        assignment = self.get_object()
        user = self.request.user
        if assignment.stop_log_time(user, notes=None):
            return Response(TaskAssignmentSerializer(assignment).data)
        return Response({'Can not start log': 'Assignment not open for logging.'}, status=status.HTTP_404_NOT_FOUND)
