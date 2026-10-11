
"""Tests for the Houston 311 citywide importer."""

import json
import runpy
import sqlite3
from pathlib import Path


IMPORTER_PATH = (
    Path(__file__).resolve().parents[1]
    / "database"
    / "import_311.py"
)

import_archive = runpy.run_path(
    str(IMPORTER_PATH)
)["import_archive"]


HEADER = (
    "365 Case Number|Case Number|Latitude|Longitude|"
    "Incident Street|Description|Extract Date|Resolution Notes "
)


def sample_archive(extract_date="2026-10-10"):
    """Create a small archive with realistic source formatting."""
    return (
        "----- Houston 311 Public Data -----\n"
        "Extract date-time: [2026-10-09 23:07:02.07]\n"
        f"{HEADER}\n"
        f"2600000001|2600000001|29.7|-95.5|MAIN ST|"
        f"Signal out|{extract_date}|Inspection scheduled\n"
        f"{HEADER}\n"
        f"2600000001|2600000001|29.7|-95.5|MAIN ST|"
        f"Signal still out|{extract_date}|Maintenance pending\n"
        "\x1a\n"
    )


def test_import_preserves_source_records(tmp_path):
    """Verify original source fields and duplicate case rows are retained."""
    archive = tmp_path / "311-2026.txt"
    database = tmp_path / "streetsignal.sqlite"

    archive.write_text(sample_archive(), encoding="utf-8")

    result = import_archive(archive, database)

    assert result[1:] == (2, 1)

    with sqlite3.connect(database) as connection:
        rows = connection.execute(
            """
            SELECT source_line_number, original_record_json
            FROM raw_311_requests
            ORDER BY source_line_number
            """
        ).fetchall()

    assert len(rows) == 2
    assert [row[0] for row in rows] == [4, 6]

    first = json.loads(rows[0][1])
    second = json.loads(rows[1][1])

    assert len(first) == 8
    assert first["Description"] == "Signal out"
    assert second["Description"] == "Signal still out"

    # Preserve the original header's trailing space.
    assert first["Resolution Notes "] == "Inspection scheduled"


def test_duplicate_import_is_skipped(tmp_path):
    """The same source archive must not be imported twice."""
    archive = tmp_path / "311-2026.txt"
    database = tmp_path / "streetsignal.sqlite"

    archive.write_text(sample_archive(), encoding="utf-8")

    import_archive(archive, database)

    assert import_archive(archive, database) is None

    with sqlite3.connect(database) as connection:
        imports = connection.execute(
            "SELECT COUNT(*) FROM source_imports"
        ).fetchone()[0]

        records = connection.execute(
            "SELECT COUNT(*) FROM raw_311_requests"
        ).fetchone()[0]

    assert imports == 1
    assert records == 2


def test_extract_date_does_not_change_content_hash(tmp_path):
    """Changing only Extract Date should not alter record content hashes."""
    database = tmp_path / "streetsignal.sqlite"

    first_archive = tmp_path / "extract_a.txt"
    second_archive = tmp_path / "extract_b.txt"

    first_archive.write_text(
        sample_archive("2026-10-10"),
        encoding="utf-8",
    )

    second_archive.write_text(
        sample_archive("2026-10-11"),
        encoding="utf-8",
    )

    import_archive(first_archive, database)
    import_archive(second_archive, database)

    with sqlite3.connect(database) as connection:
        hashes = connection.execute(
            """
            SELECT content_sha256
            FROM raw_311_requests
            ORDER BY import_id, source_line_number
            """
        ).fetchall()

    # Two source snapshots, each with the same two record versions.
    assert len(hashes) == 4
    assert hashes[:2] == hashes[2:]


def test_malformed_record_is_quarantined(tmp_path):
    """Malformed records are preserved separately without stopping imports."""
    archive = tmp_path / "broken.txt"
    database = tmp_path / "streetsignal.sqlite"

    # Remove one delimiter from the second record.
    # This produces seven fields instead of eight.
    archive.write_text(
        sample_archive().replace(
            "Signal still out|2026-10-10",
            "Signal still out 2026-10-10",
        ),
        encoding="utf-8",
    )

    result = import_archive(archive, database)

    # One valid row; one repeated header; one quarantined row.
    assert result[1:] == (1, 1)

    with sqlite3.connect(database) as connection:
        counts = connection.execute(
            """
            SELECT record_count, malformed_row_count
            FROM source_imports
            """
        ).fetchone()

        quarantined = connection.execute(
            """
            SELECT
                source_line_number,
                expected_field_count,
                actual_field_count,
                original_line
            FROM raw_311_malformed_rows
            """
        ).fetchone()

        valid_records = connection.execute(
            "SELECT COUNT(*) FROM raw_311_requests"
        ).fetchone()[0]

    assert counts == (1, 1)
    assert valid_records == 1

    assert quarantined is not None
    assert quarantined[0:3] == (6, 8, 7)

    # The exact malformed source line must be preserved.
    assert quarantined[3] == archive.read_text(
        encoding="utf-8"
    ).splitlines()[5]
