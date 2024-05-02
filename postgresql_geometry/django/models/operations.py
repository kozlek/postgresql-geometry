from __future__ import annotations

from django.contrib.postgres.operations import CreateExtension


class CubeExtension(CreateExtension):
    def __init__(self):
        super().__init__(name="cube")


class EarthDistanceExtension(CreateExtension):
    def __init__(self):
        super().__init__(name="earthdistance")
