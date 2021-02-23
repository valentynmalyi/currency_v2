from django.core.management.base import BaseCommand

from apps.history.management import init


class Command(BaseCommand):
    help = 'Init first data'

    def handle(self, *args, **kwargs):
        init.init()
