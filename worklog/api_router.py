from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from user.api.views import UserViewSet
from timekeeping.api.views import ProjectViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet)

app_name = "api"
urlpatterns = router.urls
