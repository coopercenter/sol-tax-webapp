# Generated by Django 3.1 on 2021-01-13 18:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_auto_20210113_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
