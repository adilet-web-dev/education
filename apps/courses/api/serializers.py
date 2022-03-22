from rest_framework.serializers import ModelSerializer

from apps.courses.models import Course


class CourseSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Course
