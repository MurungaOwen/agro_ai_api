from django.apps import AppConfig


class UserssConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userss'

    def ready(self):
        import userss.signals
