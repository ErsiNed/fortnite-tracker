from django.apps import AppConfig


class VbucksTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vbucks_tracker'

    def ready(self):
        import vbucks_tracker.signals
