from django.core.management.base import BaseCommand

from apps.history.management import worker_load_history_from_csv


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        worker_load_history_from_csv.main()
