# Generated by Django 3.1.1 on 2021-04-23 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
            ],
            options={
                'db_table': 'order_statuses',
            },
        ),
        migrations.CreateModel(
            name='TimeMarker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_marker', models.DateField(db_index=True, unique=True)),
            ],
            options={
                'db_table': 'time_markers',
                'ordering': ['time_marker'],
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=3)),
                ('second', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'currencies',
                'unique_together': {('first', 'second')},
                'index_together': {('first', 'second')},
            },
        ),
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('close', models.FloatField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.currency')),
                ('time_marker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.timemarker')),
            ],
            options={
                'db_table': 'bars',
                'ordering': ['time_marker'],
                'unique_together': {('time_marker', 'currency')},
                'index_together': {('time_marker', 'currency')},
            },
        ),
    ]