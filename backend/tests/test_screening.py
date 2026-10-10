
from backend.src.streetsignal.screening import screen_record


# Reference intersection used for our pilot case.
PILOT = {
    "reference_lat": 29.67429483,
    "reference_lon": -95.57049304,
    "street_a": "Bissonnet",
    "street_b": "Wilcrest",
    "text_fields": (
        "Incident Address",
        "Incident Street",
        "Description",
    ),
}


def test_nearby_record():
    """A nearby record qualifies even without street names."""
    record = {
        "Latitude": "29.67429483",
        "Longitude": "-95.57049304",
        "Description": "Traffic signal malfunction",
    }

    result = screen_record(record, **PILOT)

    assert result.is_candidate
    assert result.within_radius
    assert not result.both_streets_named
    assert result.distance_m == 0


def test_street_names_without_coordinates():
    """Text can identify candidates with missing coordinates."""
    record = {
        "Latitude": "",
        "Longitude": "",
        "Description": "Signal out at Bissonnet and Wilcrest",
    }

    result = screen_record(record, **PILOT)

    assert result.is_candidate
    assert result.both_streets_named
    assert not result.within_radius
    assert result.distance_m is None


def test_distant_unrelated_record():
    """An unrelated, distant record should not qualify."""
    record = {
        "Latitude": "29.7500",
        "Longitude": "-95.4000",
        "Description": "Damaged roadway",
    }

    result = screen_record(record, **PILOT)

    assert not result.is_candidate
    assert not result.within_radius
    assert not result.both_streets_named


def test_invalid_coordinates():
    """Invalid coordinates must not create false matches."""
    record = {
        "Latitude": "NaN",
        "Longitude": "-95.57049304",
        "Description": "Traffic signal issue",
    }

    result = screen_record(record, **PILOT)

    assert not result.is_candidate
    assert result.distance_m is None


def test_both_screening_rules():
    """A record can match geographic and textual screening."""
    record = {
        "Latitude": "29.67429483",
        "Longitude": "-95.57049304",
        "Description": "Crosswalk faded at Bissonnet and Wilcrest",
    }

    result = screen_record(record, **PILOT)

    assert result.is_candidate
    assert result.within_radius
    assert result.both_streets_named
