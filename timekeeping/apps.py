from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TimekeepingConfig(AppConfig):
    name = 'timekeeping'
    verbose_name = _("Time Keeping")
    default_auto_field = 'django.db.models.UUIDField'
