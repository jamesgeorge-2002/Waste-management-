from django.apps import AppConfig


class WasteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'waste'

    def ready(self):
        # import signals
        try:
            import waste.signals  # noqa
        except Exception:
            pass
