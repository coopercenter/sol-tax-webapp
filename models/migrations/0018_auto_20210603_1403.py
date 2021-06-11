# Generated by Django 3.1.7 on 2021-06-03 18:03

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0017_auto_20210603_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='revenue_share_rate',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[1400, 1540, 1694, 1863, 2050, 2255, 2480, 2728, 3001], size=None),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 3, 18, 3, 53, 837524, tzinfo=utc)),
        ),
    ]
