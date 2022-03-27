# Generated by Django 4.0.3 on 2022-03-27 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='users.profile'),
        ),
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_courses', to='users.profile'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='courses', to='users.profile'),
        ),
    ]
