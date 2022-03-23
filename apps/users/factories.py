import factory
from factory.fuzzy import FuzzyChoice

from django.db.models.signals import post_save

from .models import User, PROFESSION_CHOICES, StudentProfile, TeacherProfile
from apps.courses.factories import CourseFactory


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User


class TeacherFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    profession = factory.fuzzy.FuzzyChoice(PROFESSION_CHOICES)

    class Meta:
        model = TeacherProfile


class StudentFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = StudentProfile


class UserTeacherFactory(UserFactory):
    profile = factory.RelatedFactory(TeacherFactory, factory_related_name="user")


class UserStudentFactory(UserFactory):
    profile = factory.RelatedFactory(StudentFactory, factory_related_name="user")
