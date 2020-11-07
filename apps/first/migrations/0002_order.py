# Generated by Django 3.0.8 on 2020-08-30 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
        ('first', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('close_marker', models.PositiveSmallIntegerField()),
                ('result', models.FloatField()),
                ('is_buy', models.BooleanField()),
                ('time_marker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.TimeMarker')),
            ],
        ),
    ]
