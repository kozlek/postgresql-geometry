from __future__ import annotations

import pytest
from factory import Faker

from postgresql_geometry import Point
from postgresql_geometry_tests.django.factories import UserFactory


@pytest.mark.django_db()
class TestPointField:
    def test_point_field_select(self) -> None:
        user = UserFactory()
        assert isinstance(user.location, Point)
        assert isinstance(user.location.longitude, float) and isinstance(user.location.latitude, float)

    def test_point_insert(self, faker: Faker) -> None:
        point = faker.point()

        user = UserFactory(location=point)
        user.refresh_from_db()
        assert user.location == point

        user_without_location = UserFactory(location=None)
        user_without_location.refresh_from_db()
        assert user_without_location.location is None
