# Generated by Django 3.1 on 2020-10-14 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0027_auto_20201013_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='dominion_or_apco',
            field=models.BooleanField(default=True),
        ),
    ]
