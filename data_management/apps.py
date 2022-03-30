import json

from django.apps import AppConfig

from config.settings import BASE_DIR


class DataManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_management'

    def ready(self):
        from .models import Profession

        with open(f"{BASE_DIR}/default_professions.json", "r") as file:
            default_professions = json.loads(file.read())
            for profession in default_professions:
                Profession.objects.get_or_create(name=profession)
