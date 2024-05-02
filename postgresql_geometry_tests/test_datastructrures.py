from __future__ import annotations

import pytest
from faker import Faker

from postgresql_geometry.datastructures import Point


class TestPoint:
    def test_point_init(self, faker: Faker) -> None:
        longitude, latitude = faker.longitude_and_latitude()

        point = Point(longitude, latitude)
        assert point.longitude == longitude
        assert point.latitude == latitude

        point = Point(latitude=latitude, longitude=longitude)
        assert point.longitude == longitude
        assert point.latitude == latitude

    def test_point_eq(self, faker: Faker) -> None:
        longitude0, latitude0 = faker.longitude_and_latitude()
        longitude1, latitude1 = faker.longitude_and_latitude()

        point0_a = Point(longitude0, latitude0)
        point0_b = Point(latitude=latitude0, longitude=longitude0)
        assert point0_a == point0_b

        point1_a = Point(longitude1, latitude1)
        point1_b = Point(latitude=latitude1, longitude=longitude1)
        assert point1_a == point1_b

        assert point0_a != point1_a

    @pytest.mark.parametrize(
        ("string", "longitude", "latitude"),
        [
            ("()", None, None),
            ("(2.3463463, 48.881885)", 2.3463463, 48.881885),
            ("(2.3463463,48.881885)", 2.3463463, 48.881885),
            ("(2.3463463,test)", None, None),
        ],
    )
    def test_point_from_postgres_string(self, string: str, longitude: float | None, latitude: float | None) -> None:
        if longitude is None or latitude is None:
            with pytest.raises(ValueError):
                Point.from_postgres_string(string)

        else:
            point = Point.from_postgres_string(string)
            assert point.longitude == longitude
            assert point.latitude == latitude

    def test_point_to_postgres_string(self) -> None:
        point = Point(2.3463463, 48.881885)
        assert point.to_postgres_string() == "(2.3463463, 48.881885)"

    @pytest.mark.parametrize(
        ("value", "longitude", "latitude"),
        [
            ((), None, None),
            ((2.3463463, 48.881885), 2.3463463, 48.881885),
            ((2.3463463, 48.881885, 42), None, None),
            ((2.3463463,), None, None),
            ((2.3463463, "test"), None, None),
        ],
    )
    def test_point_from_tuple(
        self,
        value: tuple[float, float],
        longitude: float | None,
        latitude: float | None,
    ) -> None:
        if longitude is None or latitude is None:
            with pytest.raises(ValueError):
                Point.from_tuple(value)

        else:
            point = Point.from_tuple(value)
            assert point.longitude == longitude
            assert point.latitude == latitude

    def test_point_to_tuple(self) -> None:
        point = Point(2.3463463, 48.881885)
        assert point.to_tuple() == (2.3463463, 48.881885)
