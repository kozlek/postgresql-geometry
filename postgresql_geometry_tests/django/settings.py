from __future__ import annotations

import os
import urllib.parse

import dotenv

dotenv.load_dotenv()


def _parse_postgres_dsn(value: str, /) -> dict[str, str | int | None]:
    parsed_dsn = urllib.parse.urlparse(value, allow_fragments=False)
    return {
        "HOST": parsed_dsn.hostname,
        "PORT": parsed_dsn.port,
        "USER": parsed_dsn.username,
        "PASSWORD": parsed_dsn.password,
        "NAME": parsed_dsn.path[1:],
    }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        **_parse_postgres_dsn(os.environ.get("POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5432/postgres")),
    },
}

INSTALLED_APPS = (
    "rest_framework",
    "postgresql_geometry_tests.django",
)

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
