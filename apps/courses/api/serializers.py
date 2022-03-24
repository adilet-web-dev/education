from rest_framework.serializers import ModelSerializer

from apps.courses.models import Course, HomeworkTask, Homework


class CourseSerializer(ModelSerializer):
    class Meta:
        fields = [
            "name",
            "description",
            "profession",
            "cost",
            "cover_image",
            "youtube_link",
        ]

        model = Course


class HomeworkTaskSerializer(ModelSerializer):
    class Meta:
        fields = [
            "stage",
            "name",
            "description",
            "deadline"
        ]

        model = HomeworkTask


class HomeworkSerializer(ModelSerializer):
    class Meta:
        fields = [
            "text"
        ]

        model = Homework
