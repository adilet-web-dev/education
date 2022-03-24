from rest_framework.permissions import BasePermission
from apps.courses.models import Course


class IsCourseStudent(BasePermission):
    def has_object_permission(self, request, view, obj: Course):
        return obj.students.filter(user=request.user).exists()


class IsCourseOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Course):
        return obj.author == request.user.profile
