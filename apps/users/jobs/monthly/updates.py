from django_extensions.management.jobs import BaseJob

from apps.users.models import Profile


class UpdateMonthlyTenFreeCoursesNumberJob(BaseJob):
    help = "Give every user with base subscription ten free courses limit"

    def execute(self):
        # executing empty sample job
        for profile in Profile.objects.filter(app_subscription_mode="BASE"):
            profile.free_courses_number = 10
            profile.save()
