from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # THIS MUST HAVE THE 'apps.' PREFIX
    name = 'apps.notifications'