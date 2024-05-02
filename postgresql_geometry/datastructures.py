from __future__ import annotations

import dataclasses
import re
import typing


@dataclasses.dataclass(frozen=True, slots=True)
class Point:
    longitude: float
    latitude: float

    POSTGRES_STRING_REGEX: typing.ClassVar[re.Pattern] = re.compile(
        r"^\(([+-]?[0-9]*\.?[0-9]+), ?([+-]?[0-9]*[.]?[0-9]+)\)$",
    )

    @classmethod
    def from_postgres_string(cls, value: str, /) -> typing.Self:
        if match := cls.POSTGRES_STRING_REGEX.match(value.strip()):
            return cls(longitude=float(match[1]), latitude=float(match[2]))
        raise ValueError("Invalid postgres point string.")

    def to_postgres_string(self) -> str:
        return f"({self.longitude}, {self.latitude})"

    @classmethod
    def from_tuple(cls, value: tuple[float, float], /) -> typing.Self:
        try:
            return cls(*map(float, value))
        except TypeError as e:
            raise ValueError("Invalid tuple for point.") from e

    def to_tuple(self) -> tuple[float, float]:
        return self.longitude, self.latitude
