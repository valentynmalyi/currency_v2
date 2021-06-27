from django.core.management.base import BaseCommand

from apps.terminal.management import worker_first_open


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        worker_first_open.main()
