from __future__ import annotations

from rest_framework import serializers

from postgresql_geometry.django import models as postgresql_geometry_models
from postgresql_geometry.rest_framework.fields import PointField
from postgresql_geometry_tests.django.models import User

serializers.ModelSerializer.serializer_field_mapping |= {postgresql_geometry_models.PointField: PointField}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "location")
        read_only_fields = ("id",)
