# Generated by Django 3.1 on 2020-11-12 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0041_remove_userprofile_user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='simulation',
            name='unique_locality_simulation',
        ),
        migrations.AddConstraint(
            model_name='simulation',
            constraint=models.UniqueConstraint(fields=('user', 'initial_investment', 'initial_year', 'project_length', 'project_size', 'total_acreage', 'inside_fence_acreage', 'baseline_land_value', 'inside_fence_land_value', 'outside_fence_land_value', 'dominion_or_apco'), name='unique_user_simulation'),
        ),
    ]
