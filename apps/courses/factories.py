import factory
from factory import fuzzy
from django.utils import timezone

from .models import Course, PROFESSION_CHOICES, Homework, HomeworkTask
from apps.users.factories import ProfileFactory


class CourseFactory(factory.django.DjangoModelFactory):

    name = factory.Faker("name")
    description = factory.Faker("text")
    profession = fuzzy.FuzzyChoice(PROFESSION_CHOICES)
    cost = fuzzy.FuzzyInteger(100, 100_000)
    author = factory.SubFactory(ProfileFactory)
    youtube_link = factory.Faker("url")
    created_at = fuzzy.FuzzyDateTime(timezone.now() - timezone.timedelta(days=3), timezone.now())

    class Meta:
        model = Course


class HomeworkTaskFactory(factory.django.DjangoModelFactory):
    course = factory.SubFactory(CourseFactory)
    name = factory.Faker("name")
    description = factory.Faker("text")
    deadline = fuzzy.FuzzyDateTime(timezone.now(), timezone.now() + timezone.timedelta(days=3))

    class Meta:
        model = HomeworkTask


class HomeworkFactory(factory.django.DjangoModelFactory):
    homework_task = factory.SubFactory(HomeworkTaskFactory)
    student = factory.SubFactory(ProfileFactory)
    uploaded_at = fuzzy.BaseFuzzyDateTime(timezone.now() - timezone.timedelta(days=1), timezone.now())

    class Meta:
        model = Homework
