from __future__ import annotations

import typing

import pytest
from faker import Faker
from rest_framework import serializers

from postgresql_geometry import Point
from postgresql_geometry.rest_framework.fields import PointField
from postgresql_geometry_tests.rest_framework.serializers import UserSerializer


class _TestSerializer(serializers.Serializer):
    name = serializers.CharField()
    coordinates = PointField()


class TestPointField:
    @pytest.mark.parametrize(
        ("data", "serialized_data"),
        [
            (
                {"name": "Test", "coordinates": Point(2.3463463, 48.881885)},
                {"name": "Test", "coordinates": [2.3463463, 48.881885]},
            ),
        ],
    )
    def test_point_serialize(self, data: dict[str, typing.Any], serialized_data: dict[str, typing.Any]) -> None:
        assert _TestSerializer(data).data == serialized_data

    @pytest.mark.parametrize(
        ("serialized_data", "data", "is_valid"),
        [
            (
                {"name": "Test", "coordinates": [2.3463463, 48.881885]},
                {"name": "Test", "coordinates": Point(2.3463463, 48.881885)},
                True,
            ),
            (
                {"name": "Test", "coordinates": ["2.3463463", "48.881885"]},
                {"name": "Test", "coordinates": Point(2.3463463, 48.881885)},
                True,
            ),
            ({"name": "Test", "coordinates": [2.3463463]}, None, False),
        ],
    )
    def test_point_deserialize(
        self,
        serialized_data: dict[str, typing.Any],
        data: dict[str, typing.Any],
        is_valid: bool,
    ) -> None:
        serializer = _TestSerializer(data=serialized_data)
        assert serializer.is_valid() is is_valid
        if is_valid:
            assert serializer.validated_data == data

    @pytest.mark.django_db()
    def test_point_serialize_model_serializer(self, faker: Faker) -> None:
        location = faker.point()

        serializer = UserSerializer(data={"location": list(location.to_tuple())})
        serializer.is_valid()
        user = serializer.save()

        user.refresh_from_db()
        assert user.location == location
