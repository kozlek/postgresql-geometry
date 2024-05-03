from __future__ import annotations

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from postgresql_geometry import Point


class PointField(serializers.ListField):
    default_error_messages = {
        "size": _("Expected a 2 float items list."),
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("child", serializers.FloatField())
        kwargs.setdefault("allow_empty", False)
        super().__init__(**kwargs)

    def to_internal_value(self, data: list[float]) -> Point:
        value = super().to_internal_value(data)
        if len(value) != 2:
            self.fail("size")
        return Point.from_tuple(value)

    def to_representation(self, value: Point) -> list[float]:
        return list(value.to_tuple())
