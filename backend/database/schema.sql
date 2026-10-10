
-- StreetSignal Houston
-- Database schema v0.1
-- Citywide source ingestion and evidence preservation

PRAGMA foreign_keys = ON;

-- Track every source file imported into StreetSignal.
CREATE TABLE IF NOT EXISTS source_imports (
    id INTEGER PRIMARY KEY,

    source_name TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_sha256 TEXT NOT NULL,

    source_extract_at TEXT,
    source_headers_json TEXT NOT NULL,

    imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    record_count INTEGER NOT NULL DEFAULT 0
        CHECK (record_count >= 0),

    repeated_header_count INTEGER NOT NULL DEFAULT 0
        CHECK (repeated_header_count >= 0),

    malformed_row_count INTEGER NOT NULL DEFAULT 0
        CHECK (malformed_row_count >= 0),

    UNIQUE (source_name, file_sha256)
);


-- Preserve original Houston 311 records.
CREATE TABLE IF NOT EXISTS raw_311_requests (
    import_id INTEGER NOT NULL,
    source_line_number INTEGER NOT NULL
        CHECK (source_line_number > 0),

    -- Original case identifiers
    case_number_365 TEXT,
    case_number TEXT,

    -- Dates
    created_date_local TEXT,
    created_date_utc TEXT,
    closed_date TEXT,

    -- Classification and status
    case_type TEXT,
    status TEXT,
    state_code TEXT,
    state_code_name TEXT,
    department TEXT,
    division TEXT,

    -- Location
    incident_address TEXT,
    incident_street TEXT,
    incident_city TEXT,
    incident_state TEXT,
    zip_code TEXT,
    latitude REAL,
    longitude REAL,

    -- Fingerprint used to compare record contents
    -- across different source extracts.
    -- Excludes only the source "Extract Date" field.
    content_sha256 TEXT NOT NULL,

    -- Complete original source record as JSON.
    -- Includes all 49 original fields, including:
    -- Description, Latest Case Notes,
    -- Resolution Notes, and Extract Date.
    original_record_json TEXT NOT NULL
        CHECK (json_valid(original_record_json)),

    PRIMARY KEY (import_id, source_line_number),

    FOREIGN KEY (import_id)
        REFERENCES source_imports(id)
);


-- Look up original cases and compare versions.
CREATE INDEX IF NOT EXISTS idx_311_case_number_365
    ON raw_311_requests (
        case_number_365,
        content_sha256
    );

CREATE INDEX IF NOT EXISTS idx_311_case_number
    ON raw_311_requests (case_number);


-- Search requests chronologically.
CREATE INDEX IF NOT EXISTS idx_311_created_date
    ON raw_311_requests (created_date_local);


-- Filter by original City of Houston case type.
CREATE INDEX IF NOT EXISTS idx_311_case_type
    ON raw_311_requests (case_type);


-- Geographic filtering for any supported intersection.
CREATE INDEX IF NOT EXISTS idx_311_location
    ON raw_311_requests (latitude, longitude);
