from django.apps import AppConfig


class CustomUserConfig(AppConfig):
    name = 'custom_user'

    def ready(self):
        import custom_user.signals
