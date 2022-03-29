# Generated by Django 4.0.3 on 2022-03-28 15:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_subscription_price', models.PositiveIntegerField()),
                ('pro_subscription_price', models.PositiveIntegerField()),
                ('professions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
            ],
            options={
                'verbose_name': 'app management',
            },
        ),
    ]
