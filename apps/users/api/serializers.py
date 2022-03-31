from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField


from apps.users.models import TemporaryUser, Profile
from app_management.models import Profession


class TemporaryUserSerializer(ModelSerializer):
    class Meta:
        model = TemporaryUser
        fields = ["email", "username", "password"]


class ProfileSerializer(ModelSerializer):
    subscribers = SerializerMethodField()
    subscribes = SerializerMethodField()
    my_courses = SerializerMethodField()

    def get_subscribers(self, obj: Profile) -> int:
        return obj.subscribers.count()

    def get_subscribes(self, obj: Profile) -> int:
        return obj.subscribes.count()

    def get_my_courses(self, obj: Profile) -> int:
        return obj.my_courses.count()

    class Meta:
        model = Profile
        fields = [
            "profession",
            "rating",
            "work_experience",
            "short_info",
            "subscribers",
            "subscribes",
            "my_courses"
        ]

        read_only_fields = ["rating"]
