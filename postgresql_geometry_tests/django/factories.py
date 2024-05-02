from __future__ import annotations

import factory.django

from .models import Store, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    location = factory.Faker("point")


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    location = factory.Faker("point")
