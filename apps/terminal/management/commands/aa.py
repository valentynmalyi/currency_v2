from django.core.management.base import BaseCommand

from apps.terminal.management import worker_aa


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        worker_load_history_from_csv.main()
