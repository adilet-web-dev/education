# Generated by Django 4.0.3 on 2022-03-28 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_app_subscription_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='app_subscription_mode',
            field=models.CharField(blank=True, choices=[('pro', 'PRO'), ('base', 'BASE')], max_length=4, null=True),
        ),
    ]