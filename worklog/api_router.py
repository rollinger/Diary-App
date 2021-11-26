from django.conf import settings
from rest_framework.routers import DefaultRouter

from users.api.views import UserViewSet
from timekeeping.api.views import (
	ProjectViewSet, 
	TaskViewSet, 
	AssignmentViewSet, 
	WorklogViewSet,
	AssignmentWorkerViewSet, 
	WorklogWorkerViewSet
)

router = DefaultRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)
router.register("assignments", AssignmentViewSet)
router.register("worklogs", WorklogViewSet)
# router.register("user_assignments", AssignmentWorkerViewSet)
# router.register("user_worklogs", WorklogWorkerViewSet)

app_name = "api"
urlpatterns = router.urls
