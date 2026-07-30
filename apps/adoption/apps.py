from django.apps import AppConfig

class AdoptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.adoption'

    def ready(self):
        import apps.adoption.signals # This is the "Switch" for notifications