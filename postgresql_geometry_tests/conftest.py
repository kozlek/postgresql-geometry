from __future__ import annotations

import factory
import pytest
from faker import Faker

from postgresql_geometry.faker.providers import GeometryProvider

factory.Faker.add_provider(GeometryProvider)


@pytest.fixture(scope="session", autouse=True)
def _setup_faker_provider(_session_faker: Faker) -> None:
    _session_faker.add_provider(GeometryProvider)
