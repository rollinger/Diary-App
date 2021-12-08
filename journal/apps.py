from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JournalConfig(AppConfig):
    name = 'journal'
    verbose_name = _("Journal")
    default_auto_field = 'django.db.models.UUIDField'

    def ready(self):
        try:
            import diary.journal.signals  # noqa F401
        except ImportError:
            pass