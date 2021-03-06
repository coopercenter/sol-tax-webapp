# Generated by Django 3.1 on 2021-03-06 18:22

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0012_auto_20210223_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 6, 18, 22, 11, 557907, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='locality',
            name='local_depreciation',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True), blank=True, null=True, size=35),
        ),
    ]
