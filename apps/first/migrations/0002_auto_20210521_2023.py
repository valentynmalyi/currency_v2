# Generated by Django 3.1.1 on 2021-05-21 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='atr',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='sl',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='tp',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='volume',
            field=models.FloatField(default=None, null=True),
        ),
    ]
