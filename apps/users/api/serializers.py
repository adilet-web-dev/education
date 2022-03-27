from rest_framework.serializers import ModelSerializer

from apps.users.models import TemporaryUser


class TemporaryUserSerializer(ModelSerializer):
    class Meta:
        model = TemporaryUser
        fields = ["email", "username", "password"]
