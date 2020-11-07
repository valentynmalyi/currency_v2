# Generated by Django 3.0.8 on 2020-10-01 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_orderstatus'),
        ('first', '0013_auto_20200930_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.FloatField()),
                ('close_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.Order')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.OrderStatus')),
                ('time_marker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.TimeMarker')),
            ],
            options={
                'db_table': 'first_results',
            },
        ),
    ]
