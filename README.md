# postgresql-geometry

Types for PostgreSQL geometry datatypes, including Django integration.

## Supported types

### Point

```python
from postgresql_geometry import Point

point = Point(2.3463463, 48.881885)
print(point.longitude, point.latitude)
```

## Django integration

### Point type

Declare field mapped to a `point` datatype on PostgreSQL side (support migrations).

```python
from django.db import models

from postgresql_geometry import Point
from postgresql_geometry.django.models import PointField


class User(models.Model):
    location: Point = PointField()
```


### Point distance

Included `PointDistance` function allows approximate distance calculation (in kilometers)
between two points.

```python
from django.db import models

from postgresql_geometry import Point
from postgresql_geometry.django.models import PointDistance, PointField


class User(models.Model):
    location: Point = PointField()


class Store(models.Model):
    location: Point = PointField()


store = Store(location=Point(2.3463463, 48.881885))
user = User(location=Point(3.3463463, 42.881885))

qs = User.objects.annotate(
    store_distance=PointDistance(
        models.F("location"),
        models.Value(store.location, output_field=PointField()),
    ),
)
print(qs.first().store_distance)
```

⚠️ This function requires `cube` and `earthdistance` built-in extensions to be created first !
If you manage PG's extensions using Django migrations, you can add the provided operations to your migration file.

```python
from django.db import migrations

from postgresql_geometry.django.models.operations import CubeExtension, EarthDistanceExtension


class Migration(migrations.Migration):
    ...

    operations = [
        CubeExtension(),
        EarthDistanceExtension(),
    ]
```

## DRF integration

To enable `ModelSerializer` field auto-detection for extra fields, you can add them to
the default mapping.

```python
from postgresql_geometry.django.models import PointField
from postgresql_geometry.rest_framework.fields import PointField as PointSerializerField
from rest_framework import serializers

serializers.ModelSerializer.serializer_field_mapping |= {
    PointField: PointSerializerField,
}
```

### PointField (serializers)

Provide a serializer field for Django's `PointField`.
Point will be serialized into a list of 2 float.

```python
from postgresql_geometry.rest_framework.fields import PointField
from rest_framework import serializers


class MySerializer(serializers.Serializer):
    coordinates = PointField()
```

## Faker integration

If you want to quickly generate random `Point` instance(s), you can use the included
`Faker` provider.

```python
from faker import Faker
from postgresql_geometry.faker import GeometryProvider

fake = Faker()
fake.add_provider(GeometryProvider)

point = fake.point()
print(point)
```

If you use `factory-boy`, it's even easier to integrate with the inner `Faker` instance.

```python
import factory
from postgresql_geometry.faker import GeometryProvider

factory.Faker.add_provider(GeometryProvider)
```