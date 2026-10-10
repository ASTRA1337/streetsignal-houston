
from dataclasses import dataclass
from typing import Mapping
from enum import Enum


@dataclass(frozen=True)
class StreetMentions:
    street_a: bool
    street_b: bool

    @property
    def both(self) -> bool:
        return self.street_a and self.street_b


@dataclass(frozen=True)
class LocationEvidence:
    incident_address: StreetMentions
    incident_street: StreetMentions
    description: StreetMentions


class LocationStatus(str, Enum):
    INTERSECTION_SPECIFIC = "intersection_specific"
    NEARBY = "nearby"
    CONFLICTING_LOCATION = "conflicting_location"
    UNDETERMINED = "undetermined"


@dataclass(frozen=True)
class LocationAssessment:
    status: LocationStatus
    reasons: tuple[str, ...]
    requires_manual_review: bool = True



def extract_location_evidence(
    record: Mapping[str, str],
    *,
    street_a: str,
    street_b: str,
) -> LocationEvidence:
    """Capture street mentions separately by original source field.

    Mentions are evidence signals, not verified locations.
    """

    def mentions(field: str) -> StreetMentions:
        text = (record.get(field) or "").upper()

        return StreetMentions(
            street_a=street_a.upper() in text,
            street_b=street_b.upper() in text,
        )

    return LocationEvidence(
        incident_address=mentions("Incident Address"),
        incident_street=mentions("Incident Street"),
        description=mentions("Description"),
    )
