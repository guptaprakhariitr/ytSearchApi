from django.apps import AppConfig


class YtapiConfig(AppConfig):
    name = 'ytapi'
    def ready(self):
        from ytapi import updater
        updater.start()
        return super().ready()