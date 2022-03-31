from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import AppManagement, Profession


# Register your models here.
admin.site.register(AppManagement, SingletonModelAdmin)
admin.site.register(Profession)
