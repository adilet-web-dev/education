from django.contrib import admin
from .models import Course, HomeworkTask, Homework

# Register your models here.
admin.site.register(Course)
admin.site.register(HomeworkTask)
admin.site.register(Homework)
