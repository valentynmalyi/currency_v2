# Generated by Django 3.1.1 on 2021-02-27 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0005_remove_order_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='order',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='first.order'),
        ),
    ]
