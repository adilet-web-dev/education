# Generated by Django 4.0.3 on 2022-03-27 14:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('profession', models.CharField(choices=[('manager', 'Manager'), ('programmer', 'Programmer'), ('designer', 'Designer'), ('quality assurer', 'Quality assurer')], max_length=50)),
                ('cost', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(blank=True)),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='images/covers/', verbose_name='Front cover image')),
                ('youtube_link', models.URLField()),
                ('file', models.FileField(blank=True, help_text='upload file compressed to zip or rar', null=True, upload_to='courses_files/', validators=[django.core.validators.FileExtensionValidator(['zip', 'rar'])], verbose_name='course file')),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('file', models.FileField(blank=True, help_text='upload file compressed to zip or rar', null=True, upload_to='homework_tasks/', validators=[django.core.validators.FileExtensionValidator(['zip', 'rar'])], verbose_name='homework task file')),
                ('deadline', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_tasks', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('file', models.FileField(blank=True, help_text='upload file compressed to zip or rar', null=True, upload_to='homeworks/', validators=[django.core.validators.FileExtensionValidator(['zip', 'rar'])], verbose_name='homework file')),
                ('uploaded_at', models.DateTimeField()),
                ('homework_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='courses.homeworktask')),
            ],
        ),
    ]
