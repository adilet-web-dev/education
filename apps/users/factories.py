import factory
from django.db.models.signals import post_save
from .models import User, PROFESSION_CHOICES, Profile
from factory.fuzzy import FuzzyChoice


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User


class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    profession = FuzzyChoice(PROFESSION_CHOICES)

    class Meta:
        model = Profile


class UserWithProfileFactory(UserFactory):
    profile = factory.RelatedFactory(ProfileFactory, factory_related_name='user')

