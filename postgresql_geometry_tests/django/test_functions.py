from __future__ import annotations

import pytest
from django.db import models

from postgresql_geometry import Point
from postgresql_geometry.django.models import PointDistance, PointField
from postgresql_geometry_tests.django.factories import StoreFactory, UserFactory
from postgresql_geometry_tests.django.models import User


@pytest.mark.django_db()
class TestPointFunctions:
    def test_point_distance_sort(self) -> None:
        store = StoreFactory(location=Point(2.3463463, 48.881885))
        user0 = UserFactory(location=Point(2.344927, 48.8737493))
        user1 = UserFactory(location=Point(2.3311632, 48.7871845))
        user2 = UserFactory(location=Point(2.3537208, 48.8775893))

        qs = (
            User.objects.annotate(
                store_distance=PointDistance(
                    models.F("location"),
                    models.Value(store.location, output_field=PointField()),
                ),
            )
            .order_by(
                models.F("store_distance").asc(nulls_last=True),
            )
            .values_list("id", flat=True)
        )
        assert list(qs) == [user2.id, user0.id, user1.id]
