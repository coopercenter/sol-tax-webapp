# Generated by Django 4.2.1 on 2023-05-18 17:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0018_auto_20210603_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 18, 17, 37, 27, 836118, tzinfo=datetime.timezone.utc)),
        ),
    ]
