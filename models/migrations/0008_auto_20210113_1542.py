# Generated by Django 3.1 on 2021-01-13 20:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0007_auto_20210113_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 20, 42, 51, 341315, tzinfo=utc)),
        ),
    ]
