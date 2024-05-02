from __future__ import annotations

from faker.providers import BaseProvider

from postgresql_geometry import Point


class GeometryProvider(BaseProvider):
    def longitude_and_latitude(self) -> tuple[float, float]:
        lat, lng = self.generator.latlng()
        return float(lng), float(lat)

    def point(self) -> Point:
        return Point(*self.longitude_and_latitude())
