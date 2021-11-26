from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TimekeepingConfig(AppConfig):
    name = 'timekeeping'
    verbose_name = _("Time Keeping")
    default_auto_field = 'django.db.models.UUIDField'

    def ready(self):
        try:
            import worklog.timekeeping.signals  # noqa F401
        except ImportError:
            pass