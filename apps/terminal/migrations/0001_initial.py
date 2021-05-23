# Generated by Django 3.1.1 on 2021-04-23 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('first', '0001_initial'),
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.IntegerField(db_index=True)),
                ('sl', models.IntegerField()),
                ('tp', models.IntegerField()),
                ('first', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='first.result')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.orderstatus')),
            ],
        ),
    ]