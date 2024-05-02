from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from postgresql_geometry.datastructures import Point


class PointField(models.Field):
    description = "A datastructure to store longitude and latitude."

    def db_type(self, connection) -> str:
        return "point"

    def from_db_value(self, value: str | None, expression, connection) -> Point | None:
        if value is None:
            return value
        return Point.from_postgres_string(value)

    def to_python(self, value: Point | str | None) -> Point | None:
        if isinstance(value, Point) or value is None:
            return value

        try:
            return Point.from_postgres_string(value)
        except ValueError as e:
            raise ValidationError("Invalid point value.") from e

    def get_prep_value(self, value: Point | None) -> str | None:
        if value is None:
            return value
        return f"({value.longitude},{value.latitude})"

    def value_to_string(self, obj: models.Model) -> str:
        return self.value_from_object(obj).to_postgres_string()
