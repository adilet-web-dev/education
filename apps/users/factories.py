import factory
from django.db.models.signals import post_save
from .models import User, PROFESSION_CHOICES
from factory.fuzzy import FuzzyChoice


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


class StudentFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)


class UserTeacherFactory(UserFactory):
    profile = factory.RelatedFactory(TeacherFactory, factory_related_name="user")


class UserStudentFactory(UserFactory):
    profile = factory.RelatedFactory(StudentFactory, factory_related_name="user")
