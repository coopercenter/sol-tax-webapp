# Generated by Django 3.1 on 2020-11-10 20:58

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0037_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='adj_gross_income',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='adm',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='assessment_ratio',
            field=models.FloatField(default=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='baseline_true_value',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='budget_escalator',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='discount_rate',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='local_depreciation',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mt_tax_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='population',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='real_property_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='required_local_matching',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='revenue_share_rate',
            field=models.IntegerField(default=1400),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='scc_depreciation',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[0.9, 0.9, 0.9, 0.9, 0.8973, 0.8729, 0.85, 0.82, 0.79, 0.76, 0.73, 0.69, 0.66, 0.62, 0.58, 0.53, 0.49, 0.44, 0.38, 0.33, 0.27, 0.21, 0.14, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], size=None),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='taxable_retail_sales',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='use_composite_index',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='years_between_assessment',
            field=models.IntegerField(default=5),
        ),
    ]