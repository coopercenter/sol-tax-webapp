# Generated by Django 3.1 on 2020-11-19 17:01

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discount_rate', models.IntegerField(default=6)),
                ('revenue_share_rate', models.IntegerField(default=1400)),
                ('real_property_rate', models.FloatField(default=0)),
                ('mt_tax_rate', models.FloatField(default=0)),
                ('assessment_ratio', models.FloatField(default=100)),
                ('baseline_true_value', models.BigIntegerField(default=0)),
                ('adj_gross_income', models.BigIntegerField(default=0)),
                ('taxable_retail_sales', models.BigIntegerField(default=0)),
                ('population', models.IntegerField(default=0)),
                ('adm', models.FloatField(default=0)),
                ('required_local_matching', models.IntegerField(default=0)),
                ('budget_escalator', models.FloatField(default=0)),
                ('years_between_assessment', models.IntegerField(default=5)),
                ('use_composite_index', models.BooleanField(default=True)),
                ('local_depreciation', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True), blank=True, null=True, size=None)),
                ('scc_depreciation', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[0.9, 0.9, 0.9, 0.9, 0.8973, 0.8729, 0.85, 0.82, 0.79, 0.76, 0.73, 0.69, 0.66, 0.62, 0.58, 0.53, 0.49, 0.44, 0.38, 0.33, 0.27, 0.21, 0.14, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], size=None)),
            ],
            options={
                'verbose_name_plural': 'Localities',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discount_rate', models.IntegerField(default=6)),
                ('revenue_share_rate', models.IntegerField(default=1400)),
                ('real_property_rate', models.FloatField(default=0)),
                ('mt_tax_rate', models.FloatField(default=0)),
                ('assessment_ratio', models.FloatField(default=100)),
                ('baseline_true_value', models.BigIntegerField(default=0)),
                ('adj_gross_income', models.BigIntegerField(default=0)),
                ('taxable_retail_sales', models.BigIntegerField(default=0)),
                ('population', models.IntegerField(default=0)),
                ('adm', models.FloatField(default=0)),
                ('required_local_matching', models.IntegerField(default=0)),
                ('budget_escalator', models.FloatField(default=0)),
                ('years_between_assessment', models.IntegerField(default=5)),
                ('use_composite_index', models.BooleanField(default=True)),
                ('local_depreciation', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True), blank=True, null=True, size=None)),
                ('scc_depreciation', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[0.9, 0.9, 0.9, 0.9, 0.8973, 0.8729, 0.85, 0.82, 0.79, 0.76, 0.73, 0.69, 0.66, 0.62, 0.58, 0.53, 0.49, 0.44, 0.38, 0.33, 0.27, 0.21, 0.14, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], size=None)),
            ],
            options={
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('initial_investment', models.IntegerField(default=100000000)),
                ('initial_year', models.IntegerField(default=2021)),
                ('project_length', models.IntegerField(default=30)),
                ('project_size', models.IntegerField(default=100)),
                ('total_acreage', models.IntegerField(default=2000)),
                ('inside_fence_acreage', models.IntegerField(default=1000)),
                ('baseline_land_value', models.IntegerField(default=1000)),
                ('inside_fence_land_value', models.IntegerField(default=10000)),
                ('outside_fence_land_value', models.IntegerField(default=1000)),
                ('dominion_or_apco', models.BooleanField(default=True)),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='models.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Calculations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cas_mt', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None)),
                ('cas_rs', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None)),
                ('tot_mt', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None)),
                ('tot_rs', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(blank=True, null=True), blank=True, size=None)),
                ('simulation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='models.simulation')),
            ],
            options={
                'verbose_name_plural': 'Calculations',
            },
        ),
        migrations.AddConstraint(
            model_name='simulation',
            constraint=models.UniqueConstraint(fields=('user', 'name', 'initial_investment', 'initial_year', 'project_length', 'project_size', 'total_acreage', 'inside_fence_acreage', 'baseline_land_value', 'inside_fence_land_value', 'outside_fence_land_value', 'dominion_or_apco'), name='unique_locality_simulation'),
        ),
    ]
