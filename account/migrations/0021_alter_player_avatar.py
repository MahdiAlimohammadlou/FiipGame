# Generated by Django 5.0.6 on 2024-08-01 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_player_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='avatar',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.avatar'),
        ),
    ]
