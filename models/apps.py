from django.apps import AppConfig

class ModelsConfig(AppConfig):
    name = 'models'

    def ready(self):
        from . import feedback_sender
        feedback_sender.cronjob()
