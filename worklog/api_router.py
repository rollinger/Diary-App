from django.conf import settings
from rest_framework.routers import DefaultRouter

from users.api.views import UserViewSet
from timekeeping.api.views import (
	ProjectViewSet, 
	TaskViewSet, 
	TaskAssignmentViewSet, 
	UserTaskAssignmentViewSet
)

router = DefaultRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)
router.register("taskassignments", TaskAssignmentViewSet)
router.register("user_worklogs", UserTaskAssignmentViewSet)

app_name = "api"
urlpatterns = router.urls
