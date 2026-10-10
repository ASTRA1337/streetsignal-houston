
import math
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ScreeningResult:
    within_radius: bool
    both_streets_named: bool
    distance_m: float | None

    @property
    def is_candidate(self) -> bool:
        return self.within_radius or self.both_streets_named


def distance_m(
    lat: float,
    lon: float,
    reference_lat: float,
    reference_lon: float,
) -> float:
    """Calculate great-circle distance between two coordinates."""
    radius = 6_371_000

    a1 = math.radians(reference_lat)
    a2 = math.radians(lat)
    da = a2 - a1
    dl = math.radians(lon - reference_lon)

    a = (
        math.sin(da / 2) ** 2
        + math.cos(a1) * math.cos(a2) * math.sin(dl / 2) ** 2
    )

    return 2 * radius * math.asin(min(1.0, math.sqrt(a)))


def screen_record(
    record: Mapping[str, str],
    *,
    reference_lat: float,
    reference_lon: float,
    street_a: str,
    street_b: str,
    text_fields: tuple[str, ...],
    radius_m: float = 500,
) -> ScreeningResult:
    """Screen a record for review, without verifying its location."""

    distance = None

    try:
        lat = float(record["Latitude"])
        lon = float(record["Longitude"])

        if (
            math.isfinite(lat)
            and math.isfinite(lon)
            and -90 <= lat <= 90
            and -180 <= lon <= 180
        ):
            distance = distance_m(
                lat, lon, reference_lat, reference_lon
            )

    except (ValueError, TypeError, KeyError):
        pass

    within_radius = (
        distance is not None and distance <= radius_m
    )

    combined = " ".join(
        record.get(field, "") for field in text_fields
    ).upper()

    both_streets_named = (
        street_a.upper() in combined
        and street_b.upper() in combined
    )

    return ScreeningResult(
        within_radius=within_radius,
        both_streets_named=both_streets_named,
        distance_m=distance,
    )
