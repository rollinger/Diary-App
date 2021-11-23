from django.conf import settings
from rest_framework.routers import DefaultRouter

from user.api.views import UserViewSet
from timekeeping.api.views import (
	ProjectViewSet, 
	TaskViewSet, 
	AssignmentViewSet, 
	WorklogViewSet
)

router = DefaultRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)
router.register("assignments", AssignmentViewSet)
router.register("worklog", WorklogViewSet)

app_name = "api"
urlpatterns = router.urls
