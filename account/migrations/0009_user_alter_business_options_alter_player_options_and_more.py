# Generated by Django 5.0.6 on 2024-07-21 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_player_api_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_seller', models.BooleanField(default=False)),
                ('is_buyer', models.BooleanField(default=False)),
                ('is_agent', models.BooleanField(default=False)),
                ('is_guest', models.BooleanField(default=True)),
                ('otp_code', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
                ('is_phone_verified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'account_user',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='business',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='playerbusiness',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='business',
            name='business_image',
            field=models.ImageField(default=1, upload_to='Business_images/'),
            preserve_default=False,
        ),
    ]
