import factory

from .models import Profession, AppManagement


class ProfessionFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Profession
