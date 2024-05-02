from __future__ import annotations

import typing

from django.db import models

from postgresql_geometry import Point
from postgresql_geometry.django.models import PointField


class User(models.Model):
    if typing.TYPE_CHECKING:
        objects: models.Manager

    location: Point = PointField(null=True)


class Store(models.Model):
    if typing.TYPE_CHECKING:
        objects: models.Manager

    location: Point = PointField()
