from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class JournalConfig(AppConfig):
    name = 'journal'
    verbose_name = _("Journal")

    def ready(self):
        import journal.signals