# Generated by Django 3.1.1 on 2021-04-23 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.IntegerField()),
            ],
            options={
                'db_table': 'first_orders',
                'ordering': ['time_marker'],
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('abs_correlation', models.FloatField()),
                ('n', models.PositiveSmallIntegerField()),
                ('history_size', models.PositiveSmallIntegerField()),
                ('min_similar', models.PositiveSmallIntegerField()),
                ('take', models.FloatField()),
                ('mean_min', models.FloatField()),
                ('sd_min', models.FloatField()),
                ('mean_max', models.FloatField()),
                ('sd_max', models.FloatField()),
                ('n_min', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'first_settings',
            },
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.currency')),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.setting')),
            ],
            options={
                'db_table': 'first_strategies',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_buy', models.BooleanField()),
                ('n', models.PositiveSmallIntegerField()),
                ('forecast', models.FloatField()),
                ('profit', models.FloatField(default=0)),
                ('sd', models.FloatField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='first.order')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='history.orderstatus')),
                ('time_marker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.timemarker')),
            ],
            options={
                'db_table': 'first_results',
                'ordering': ['time_marker'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='strategy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='first.strategy'),
        ),
        migrations.AddField(
            model_name='order',
            name='time_marker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.timemarker'),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('strategy', 'time_marker')},
        ),
    ]
