# Generated by Django 3.1 on 2020-09-30 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0012_locality_real_propery_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='adj_gross_income',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='locality',
            name='adm',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='locality',
            name='assesment_ratio',
            field=models.FloatField(default=100),
        ),
        migrations.AddField(
            model_name='locality',
            name='baseline_true_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='locality',
            name='budget_escalator',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='locality',
            name='population',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='locality',
            name='required_local_matching',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='locality',
            name='taxable_retail_sales',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='simulation',
            name='baseline_land_value',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='simulation',
            name='inside_fence_acerage',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='simulation',
            name='inside_fence_land_value',
            field=models.IntegerField(default=10000),
        ),
        migrations.AddField(
            model_name='simulation',
            name='total_acerage',
            field=models.IntegerField(default=2000),
        ),
    ]