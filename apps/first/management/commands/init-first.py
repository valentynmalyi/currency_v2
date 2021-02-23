from django.core.management.base import BaseCommand

from apps.first.management import init


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        init.init()
