# Generated by Django 5.0.6 on 2024-06-23 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_player_last_coin_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('base_profit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('upgrade_cost_factor', models.DecimalField(decimal_places=2, default=1.15, max_digits=5)),
                ('category', models.CharField(choices=[('shop', 'Shop'), ('company', 'Company'), ('manufacturing', 'Manufacturinfg'), ('import', 'Import'), ('mine', 'Mine'), ('factory', 'Factory')], max_length=20)),
                ('ranking', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level', models.IntegerField(default=1)),
                ('profit', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.business')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.player')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
