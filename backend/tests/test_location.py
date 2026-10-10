
from backend.src.streetsignal.location import extract_location_evidence


STREETS = {
    "street_a": "Bissonnet",
    "street_b": "Wilcrest",
}


def test_both_streets_in_address():
    """Both streets appear in concatenated address fields."""
    record = {
        "Incident Address": (
            "10900 BISSONNET ST 9600 S WILCREST DR "
            "9550 WILCREST DR 77099"
        ),
        "Incident Street": (
            "10900 BISSONNET ST 9600 S WILCREST DR "
            "9550 WILCREST DR"
        ),
        "Description": "",
    }

    result = extract_location_evidence(record, **STREETS)

    assert result.incident_address.both
    assert result.incident_street.both
    assert not result.description.both


def test_nearby_boone_road():
    """Bissonnet/Boone Road must not match Wilcrest."""
    record = {
        "Incident Address": "11000 BISSONNET ST 9600 BOONE RD",
        "Incident Street": "11000 BISSONNET ST 9600 BOONE RD",
        "Description": "",
    }

    result = extract_location_evidence(record, **STREETS)

    assert result.incident_address.street_a
    assert not result.incident_address.street_b
    assert not result.incident_address.both


def test_wilcrest_only():
    """A Wilcrest address alone does not establish the intersection."""
    record = {
        "Incident Address": "9520 WILCREST DR HOUSTON 77099",
        "Incident Street": "9520 WILCREST DR",
        "Description": "",
    }

    result = extract_location_evidence(record, **STREETS)

    assert not result.incident_address.street_a
    assert result.incident_address.street_b
    assert not result.incident_address.both


def test_description_differs_from_address():
    """Preserve potentially conflicting location signals."""
    record = {
        "Incident Address": "11000 BISSONNET ST 9600 BOONE RD",
        "Incident Street": "11000 BISSONNET ST 9600 BOONE RD",
        "Description": (
            "Traffic signal issue at Bissonnet and Wilcrest"
        ),
    }

    result = extract_location_evidence(record, **STREETS)

    assert not result.incident_address.both
    assert not result.incident_street.both
    assert result.description.both


def test_missing_location_fields():
    """Missing fields must not cause an exception."""
    record = {}

    result = extract_location_evidence(record, **STREETS)

    assert not result.incident_address.both
    assert not result.incident_street.both
    assert not result.description.both
