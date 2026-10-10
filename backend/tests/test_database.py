
"""Tests for the StreetSignal Houston database schema."""

import json
import sqlite3
from pathlib import Path

import pytest


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "database"
    / "schema.sql"
)


def create_test_database():
    """Initialize a temporary in-memory SQLite database."""
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        SCHEMA_PATH.read_text(encoding="utf-8")
    )
    return connection


def test_database_schema():
    """Verify required tables, columns, and indexes exist."""
    with create_test_database() as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'table'"
            )
        }

        assert "source_imports" in tables
        assert "raw_311_requests" in tables

        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(raw_311_requests)"
            )
        }

        assert {
            "case_number_365",
            "case_number",
            "incident_street",
            "case_type",
            "latitude",
            "longitude",
            "content_sha256",
            "original_record_json",
        }.issubset(columns)

        indexes = {
            row[1]
            for row in connection.execute(
                "PRAGMA index_list(raw_311_requests)"
            )
        }

        assert "idx_311_location" in indexes
        assert "idx_311_case_number_365" in indexes


def test_duplicate_case_numbers_are_preserved():
    """Different source rows can share a case number."""
    with create_test_database() as connection:
        cursor = connection.execute(
            """
            INSERT INTO source_imports (
                source_name,
                filename,
                file_sha256,
                source_headers_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Houston 311",
                "2026.txt",
                "example-file-hash",
                '["365 Case Number", "Description"]',
            ),
        )

        import_id = cursor.lastrowid

        for line_number, description in (
            (7, "Original report"),
            (8, "Updated report"),
        ):
            record = {
                "365 Case Number": "2600000001",
                "Description": description,
            }

            connection.execute(
                """
                INSERT INTO raw_311_requests (
                    import_id,
                    source_line_number,
                    case_number_365,
                    content_sha256,
                    original_record_json
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    import_id,
                    line_number,
                    "2600000001",
                    "example-content-hash",
                    json.dumps(record),
                ),
            )

        rows = connection.execute(
            """
            SELECT original_record_json
            FROM raw_311_requests
            WHERE case_number_365 = ?
            ORDER BY source_line_number
            """,
            ("2600000001",),
        ).fetchall()

        assert len(rows) == 2

        descriptions = [
            json.loads(row[0])["Description"]
            for row in rows
        ]

        assert descriptions == [
            "Original report",
            "Updated report",
        ]


def test_invalid_json_is_rejected():
    """Raw 311 records must contain valid JSON."""
    with create_test_database() as connection:
        connection.execute(
            """
            INSERT INTO source_imports (
                source_name,
                filename,
                file_sha256,
                source_headers_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Houston 311",
                "2026.txt",
                "example-file-hash",
                "[]",
            ),
        )

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO raw_311_requests (
                    import_id,
                    source_line_number,
                    content_sha256,
                    original_record_json
                )
                VALUES (?, ?, ?, ?)
                """,
                (1, 7, "example-hash", "not valid json"),
            )
