from django.apps import AppConfig


class DatasetConfig(AppConfig):
    name = 'csv_analyzer.apps.dataset'

    def ready(self):
        try:
            import csv_analyzer.apps.dataset.signals  # noqa F401
        except ImportError:
            pass
