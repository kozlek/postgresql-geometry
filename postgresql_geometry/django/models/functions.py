from __future__ import annotations

from django.db import models


class PointDistance(models.Func):
    template = "(%(expressions)s) * 1.609344"
    arg_joiner = " <@> "
    arity = 2
    output_field = models.FloatField()
