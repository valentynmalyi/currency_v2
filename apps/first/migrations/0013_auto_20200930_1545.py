# Generated by Django 3.0.8 on 2020-09-30 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
        ('first', '0012_auto_20200930_1540'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('strategy', 'time_marker')},
        ),
    ]
