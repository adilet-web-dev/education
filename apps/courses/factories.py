import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from .models import Course, PROFESSION_CHOICES


class CourseFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    profession = FuzzyChoice(PROFESSION_CHOICES)
    cost = FuzzyInteger(100, 10_000)

    class Meta:
        model = Course
