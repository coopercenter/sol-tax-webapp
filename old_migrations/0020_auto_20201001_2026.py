# Generated by Django 3.1 on 2020-10-02 00:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0019_auto_20201001_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculations',
            name='cas_mt',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='calculations',
            name='cas_rs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='calculations',
            name='tot_mt',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='calculations',
            name='tot_rs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None),
        ),
    ]