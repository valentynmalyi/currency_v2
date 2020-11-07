import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'currency.settings'
django.setup()