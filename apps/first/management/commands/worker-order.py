from django.core.management.base import BaseCommand

from apps.first.management import workers


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        workers.worker_order()
