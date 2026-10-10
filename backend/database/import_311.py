
"""Import original Houston 311 pipe-delimited archives into SQLite."""

import argparse
import hashlib
import json
import sqlite3
from pathlib import Path


SCHEMA_PATH = Path(__file__).with_name("schema.sql")
DEFAULT_DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "streetsignal.sqlite"
)

SOURCE_NAME = "Houston 311"
BATCH_SIZE = 2_000

REQUIRED_HEADERS = {
    "365 Case Number",
    "Case Number",
    "Latitude",
    "Longitude",
}


def file_sha256(path: Path) -> str:
    """Calculate a source file's SHA-256 checksum."""
    digest = hashlib.sha256()

    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def coordinate(value: str, lower: float, upper: float) -> float | None:
    """Convert valid source coordinates to numbers."""
    if not value.strip():
        return None

    try:
        result = float(value)
    except ValueError:
        return None

    return result if lower <= result <= upper else None


def import_archive(
    source_path: Path,
    database_path: Path,
) -> tuple[int, int, int] | None:
    """Import one complete archive, preserving original rows and fields."""

    source_path = source_path.resolve()

    if not source_path.is_file():
        raise FileNotFoundError(source_path)

    checksum = file_sha256(source_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            SCHEMA_PATH.read_text(encoding="utf-8")
        )

        existing = connection.execute(
            """
            SELECT id
            FROM source_imports
            WHERE source_name = ?
              AND file_sha256 = ?
            """,
            (SOURCE_NAME, checksum),
        ).fetchone()

        if existing:
            print(
                f"Already imported: {source_path.name} "
                f"(import {existing[0]})"
            )
            return None

        with source_path.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as source:

            extract_time = None

            for line_number, line in enumerate(source, start=1):
                text = line.rstrip("\r\n")

                if (
                    text.startswith("Extract date-time: [")
                    and text.endswith("]")
                ):
                    extract_time = text.split("[", 1)[1][:-1]

                if text.startswith("365 Case Number|"):
                    header_line = text
                    headers = text.split("|")
                    break
            else:
                raise ValueError("No Houston 311 header found")

            if (
                len(headers) != len(set(headers))
                or not REQUIRED_HEADERS.issubset(headers)
            ):
                raise ValueError(
                    "Missing or duplicated expected source headers"
                )

            connection.execute("BEGIN IMMEDIATE")

            result = connection.execute(
                """
                INSERT INTO source_imports (
                    source_name,
                    filename,
                    file_sha256,
                    source_extract_at,
                    source_headers_json
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    SOURCE_NAME,
                    source_path.name,
                    checksum,
                    extract_time,
                    json.dumps(headers, ensure_ascii=False),
                ),
            )

            import_id = result.lastrowid
            batch = []
            count = 0
            repeated_headers = 0

            insert_sql = """
                INSERT INTO raw_311_requests (
                    import_id,
                    source_line_number,
                    case_number_365,
                    case_number,
                    created_date_local,
                    created_date_utc,
                    closed_date,
                    case_type,
                    status,
                    state_code,
                    state_code_name,
                    department,
                    division,
                    incident_address,
                    incident_street,
                    incident_city,
                    incident_state,
                    zip_code,
                    latitude,
                    longitude,
                    content_sha256,
                    original_record_json
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """

            for line_number, line in enumerate(
                source,
                start=line_number + 1,
            ):
                text = line.rstrip("\r\n")

                # Ignore blank lines and the source's EOF marker.
                if text in ("", "\x1a"):
                    continue

                # The 2026 archive repeats its header 11 times.
                if text == header_line:
                    repeated_headers += 1
                    continue

                values = text.split("|")

                # Never silently discard malformed source records.
                if len(values) != len(headers):
                    raise ValueError(
                        f"Invalid row at source line {line_number}: "
                        f"expected {len(headers)} values, "
                        f"got {len(values)}"
                    )

                record = dict(zip(headers, values))

                # Extract Date changes between snapshots without
                # necessarily changing the underlying service request.
                canonical = {
                    key: value
                    for key, value in record.items()
                    if key != "Extract Date"
                }

                content_hash = hashlib.sha256(
                    json.dumps(
                        canonical,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest()

                batch.append(
                    (
                        import_id,
                        line_number,
                        record.get("365 Case Number"),
                        record.get("Case Number"),
                        record.get("Created Date Local"),
                        record.get("Created Date UTC"),
                        record.get("Closed Date"),
                        record.get("Incident Case Type"),
                        record.get("Status"),
                        record.get("State Code"),
                        record.get("State Code Name"),
                        record.get("Department"),
                        record.get("Division"),
                        record.get("Incident Address"),
                        record.get("Incident Street"),
                        record.get("Incident City"),
                        record.get("Incident State"),
                        record.get("Zip Code"),
                        coordinate(
                            record.get("Latitude", ""), -90, 90
                        ),
                        coordinate(
                            record.get("Longitude", ""), -180, 180
                        ),
                        content_hash,
                        json.dumps(
                            record,
                            ensure_ascii=False,
                            separators=(",", ":"),
                        ),
                    )
                )

                if len(batch) == BATCH_SIZE:
                    connection.executemany(insert_sql, batch)
                    count += len(batch)
                    batch.clear()

            if batch:
                connection.executemany(insert_sql, batch)
                count += len(batch)

            connection.execute(
                """
                UPDATE source_imports
                SET record_count = ?,
                    repeated_header_count = ?
                WHERE id = ?
                """,
                (count, repeated_headers, import_id),
            )

            connection.commit()

    print(
        f"Imported {count:,} 311 rows; "
        f"skipped {repeated_headers} repeated headers"
    )

    return import_id, count, repeated_headers


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "archive",
        type=Path,
        help="Original Houston 311 .txt archive",
    )

    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
    )

    args = parser.parse_args()

    import_archive(args.archive, args.db)


if __name__ == "__main__":
    main()
