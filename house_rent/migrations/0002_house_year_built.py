# Generated by Django 5.1.5 on 2025-02-09 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house_rent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='year_built',
            field=models.PositiveIntegerField(default=2000),
        ),
    ]
