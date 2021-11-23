from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from user.api.views import UserViewSet
from timekeeping.api.views import ProjectViewSet, TaskViewSet

router = DefaultRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)

app_name = "api"
urlpatterns = router.urls
