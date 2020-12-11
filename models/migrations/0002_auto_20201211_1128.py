# Generated by Django 3.1 on 2020-12-11 16:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locality',
            name='scc_depreciation',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[0.9, 0.9, 0.9, 0.9, 0.8973, 0.8729, 0.85, 0.82, 0.79, 0.76, 0.73, 0.69, 0.66, 0.62, 0.58, 0.53, 0.49, 0.44, 0.38, 0.33, 0.27, 0.21, 0.14, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], size=None),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='scc_depreciation',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[0.9, 0.9, 0.9, 0.9, 0.8973, 0.8729, 0.85, 0.82, 0.79, 0.76, 0.73, 0.69, 0.66, 0.62, 0.58, 0.53, 0.49, 0.44, 0.38, 0.33, 0.27, 0.21, 0.14, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], size=None),
        ),
    ]
