
"""Screen Houston 311 pipe-delimited archives for Bissonnet/Wilcrest review candidates.

Research screening ONLY. Nearby points and street-name mentions are not
proof of an infrastructure issue at the intersection. Stdlib-only.
"""

import csv
from streetsignal.screening import screen_record
import sys
from collections import Counter
from pathlib import Path

# CRIS intersection reference point; not a verified exact physical location.
REFERENCE_LAT, REFERENCE_LON = 29.67429483, -95.57049304
SCREENING_RADIUS_M = 500  # Exploratory search, NOT the final matching rule.

NAME_FIELDS = (
    "Incident Address",
    "Incident Street",
    "Title",
    "Description",
    "Latest Case Notes",
    "Resolution Notes",
)

EXPORT_FIELDS = (
    "365 Case Number",
    "Case Number",
    "Created Date Local",
    "Closed Date",
    "Incident Case Type",
    "Status",
    "Incident Address",
    "Latitude",
    "Longitude",
    "Title",
    "Description",
    "Latest Case Notes",
    "Resolution Notes",
)





def main(source):
    if not source.is_file():
        raise SystemExit(f"File not found: {source}")

    target = source.with_name(
        f"streetsignal_311_candidates_{source.stem}.csv"
    )

    counts = Counter()
    types = Counter()
    earliest, latest = None, None
    seen_cases = set()

    with source.open(
        "r", encoding="utf-8-sig", errors="replace", newline=""
    ) as src:

        # Houston files start with a report banner, then the header.
        for line in src:
            if line.startswith("365 Case Number|"):
                headers = [
                    column.strip()
                    for column in line.rstrip("\r\n").split("|")
                ]
                break
        else:
            raise SystemExit(
                "Cannot locate 311 column header; inspect the file first."
            )

        required = set(EXPORT_FIELDS) | set(NAME_FIELDS)
        missing = required - set(headers)

        if missing:
            raise SystemExit(
                f"Missing expected columns: {sorted(missing)}"
            )

        with target.open(
            "w", encoding="utf-8-sig", newline=""
        ) as dst:

            output = csv.DictWriter(
                dst,
                fieldnames=(
                    *EXPORT_FIELDS,
                    "screening_reason",
                    "distance_m",
                ),
            )
            output.writeheader()

            for line in src:
                if not line.strip():
                    continue

                parts = line.rstrip("\r\n").split("|")

                if len(parts) != len(headers):
                    counts["malformed"] += 1
                    continue

                counts["valid"] += 1
                rec = dict(zip(headers, parts))

                case = rec["365 Case Number"].strip()

                if case in seen_cases:
                    counts["duplicate_case_rows"] += 1

                seen_cases.add(case)

                day = rec["Created Date Local"][:10]

                if len(day) == 10 and day[4] == "-":
                    earliest = (
                        min(earliest, day) if earliest else day
                    )
                    latest = (
                        max(latest, day) if latest else day
                    )
                result = screen_record(
                    rec,
                    reference_lat=REFERENCE_LAT,
                    reference_lon=REFERENCE_LON,
                    street_a="Bissonnet",
                    street_b="Wilcrest",
                    text_fields=NAME_FIELDS,
                    radius_m=SCREENING_RADIUS_M,
                )

                distance = result.distance_m
                nearby = result.within_radius
                named = result.both_streets_named


                if not (nearby or named):
                    continue

                counts["candidates"] += 1
                counts["nearby"] += bool(nearby)
                counts["named"] += bool(named)

                types[rec["Incident Case Type"]] += 1

                output.writerow({
                    **{k: rec[k] for k in EXPORT_FIELDS},
                    "screening_reason": "+".join(
                        x for ok, x in (
                            (nearby, "within_500m"),
                            (named, "both_streets_named"),
                        )
                        if ok
                    ),
                    "distance_m": (
                        round(distance, 1)
                        if distance is not None
                        else ""
                    ),
                })

    print(f"Source: {source.name}")

    print(
        f"Rows read: {counts['valid']:,}; "
        f"malformed rows skipped: {counts['malformed']:,}"
    )

    print(f"Date range in valid rows: {earliest} to {latest}")

    print(
        f"Repeated case-number rows: "
        f"{counts['duplicate_case_rows']:,}"
    )

    print(
        f"Candidates for human review: {counts['candidates']:,} "
        f"({counts['nearby']:,} within 500 m, "
        f"{counts['named']:,} mention both streets; "
        f"groups overlap)"
    )

    print("Top candidate categories:")

    for category, count in types.most_common(12):
        print(f"  {count:>5}  {category}")

    print(f"Candidate CSV: {target}")

    if counts["malformed"]:
        print(
            "WARNING: Rows with unexpected column counts "
            "were skipped; audit before interpreting totals."
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: python extract_311_candidates.py "
            "<full-path-to-311-txt-file>"
        )

    main(Path(sys.argv[1]))
