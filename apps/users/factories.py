import factory
from factory.fuzzy import FuzzyChoice
from django.db.models.signals import post_save

from .models import User, Profile
from data_management.factories import ProfessionFactory


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User


class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    profession = factory.SubFactory(ProfessionFactory)

    class Meta:
        model = Profile


class UserWithProfileFactory(UserFactory):
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')

