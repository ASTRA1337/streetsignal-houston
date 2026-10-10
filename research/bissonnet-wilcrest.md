
# Street Safety Case: Bissonnet St & Wilcrest Dr

**StreetSignal Houston | Pilot research baseline v0.1**  
**Research updated:** 2026-10-10  
**Case status:** Research in progress; evidence consolidation complete for initial implementation handoff  
**This is not a current roadway inspection, independent engineering assessment, or finding of causation.**

## Location

- **City:** Houston, Texas
- **Intersection:** Bissonnet Street and Wilcrest Drive (also reported as S Wilcrest Drive)
- **Scope:** The intersection and immediately adjacent approaches. Different datasets have different spatial boundaries.
- **Pilot purpose:** Produce an auditable, source-linked historical Street Safety Case; validate processing rules before building a general-purpose application.

**Research question:** What crashes, infrastructure concerns, City responses, and planned interventions have been documented here, and what remains unverified?

### Why this intersection was selected

The 2019 audit's historical background includes Bissonnet/Wilcrest as **number 8** on a priority list derived by LINK Houston from 2013–2017 pedestrian/bicycle-involved crashes; the location was selected for the City's Safer Streets audit initiative. This was a defensible pilot choice based on an existing official investigation, not a new StreetSignal ranking of Houston intersections. See **2019 RSA**, background around report p. 3 and intersection section around report pp. 21–22.

- Official 2019 RSA: https://houstontx.gov/visionzero/pdf/20190520-Houston%20RSA%20part%202-SR.pdf
- Official September 2019 Safer Streets briefing: https://www.houstontx.gov/council/committees/tti/20190905/Safer-Streets-Update.pdf

## 1. Documented Crash History

**Dataset:** User-generated TxDOT CRIS Query Builder crash, unit and person CSV exports, as of **2026-10-09**, query years **2016–2026**, with a user-drawn approximately 0.05 mile by 0.05 mile search polygon centered on Bissonnet/Wilcrest. The polygon includes approaches and potentially nearby nonintersection events.

| Measure | Extracted result |
|---|---:|
| Crash records / unique crash IDs | 246 |
| Units | 519 |
| Person rows | 699 |
| Crashes labeled fatal | 2 |
| Crashes labeled suspected serious injury | 10 |
| Pedestrian-involved crash IDs / pedestrian person records | 9 / 9 |
| Pedestrian deaths in person export | 2 |
| Suspected serious pedestrian injuries in person export | 3 |

**Important qualifications:** 95 crash rows are labeled `INTERSECTION`, 63 `INTERSECTION RELATED`, 82 `NON INTERSECTION`, and 6 `DRIVEWAY ACCESS`. These fields must be preserved, not collapsed into 'intersection crashes.' Repeated coordinates likely reflect geocoding practices, not precise incident locations. One crash has no corresponding person row in the exported person table (`20141387`); the reason is not established. TxDOT warns that its data is subject to limitations and processing updates.

**Primary local exports:** `my_list (1).csv` (crashes), `CRIS Unit.csv`, `CRIS_person.csv`. Maintain the query provenance, filters and export date with these records. Do not publish every raw input in the repository automatically.

The September 11, 2026 pedestrian death is described separately by HPD near Bissonnet/Wilcrest. The release describes an investigation, not an established road-design cause: https://www.houstontx.gov/police/nr/2026/sep/nr091126-5.htm

## 2. Houston 311 Service Requests

Eight annual Houston 311 *candidate* extracts were produced with `research/extract_311_candidates.py`. Its inclusion rule is **within 500 meters of a preliminary CRIS coordinate OR text mentions both Bissonnet and Wilcrest**. This rule is for discovery; it is **not sufficient for declaring an intersection-specific issue**. All counts below reflect matching rows in the uploaded candidate files, not distinct malfunctions, accepted claims, or complete citywide annual counts.

| Year | Candidate rows | Unique candidate case numbers | Text mentions both streets | Candidate date range |
|---|---:|---:|---:|---|
| 2019 | 215 | 215 | 46 | Jan 6–Dec 29 |
| 2020 | 154 | 154 | 33 | Jan 8–Dec 30 |
| 2021 | 179 | 179 | 22 | Jan 4–Dec 30 |
| 2022 | 154 | 154 | 24 | Jan 5–Dec 28 |
| 2023 | 160 | 160 | 21 | Jan 1–Dec 31 |
| 2024 | 192 | 192 | 38 | Jan 8–Dec 26 |
| 2025 | 252 | 252 | 41 | Jan 2–Dec 24 |
| 2026 YTD | 131 | 131 | 28 | Jan 6–Oct 5 |
| **Total** | **1,437** | **1,437 unique across all eight extracts** | **253** | **Not identical year lengths** |

**Important:** The ranges above are minimum/maximum dates **among candidates only**; they do not establish full calendar-year coverage of each raw archive. The 2021 full-year archive replaces the separately obtained July–December-only extract in annual totals; never add the 92 partial-year candidates to the 179 full-year candidates. The 2026 archive is year-to-date, not directly comparable to complete years. The old and new 2021 extract versions contain timestamp and note differences that should be retained as provenance.

### Selected source-traceable examples (NOT a complete validated incident register)

| Date | Public 311 case no. | Content of the public request / recorded response | What it can establish |
|---|---|---|---|
| 2019-01-31 | `101003358978` | Pedestrian signal pole reported rotated, with signal heads difficult to see. | Reported signal-visibility concern at location; outcome unknown. |
| 2019-06-14 | `101003531136` | Pedestrian signal reported not working. | Reported concern; repair not proven from this extract. |
| 2020-02-24 | `101003877046` | A vehicle was reportedly involved in damage to a light pole and loss of signal power. | Request describes a particular event; no independent crash linkage established. |
| 2021-01-25 | `101004503961` | Lights above traffic signals reported out. | Citizen lighting report; physical outcome unknown. |
| 2021-06-26 | `101004705850` | Intersection signal lights reported out. | Citizen signal report; physical outcome unknown. |
| 2022-08-21 | `2200560677` | City technician note reports signals out, then replacement of a 30-amp breaker and restored cycling. | City-documented maintenance action on that visit. |
| 2022-09-29 | `2200609142` | Technician note says 24-volt power supply was replaced and operations checked. | City-documented equipment work on that visit. |
| 2023-07-29 | `2300957585` | Complaint reports faded arrows, stop bars and crosswalk lines. | Citizen report of markings condition; repainting unverified. |
| 2023-08-15 | `2300979238` | Complaint reports faded crosswalk markings. | Another request, not necessarily another physical issue. |
| 2024-03-08 | `2400091073` | City note states traffic-signal equipment repaired and operational. | Recorded response; does not prove permanent defect elimination. |
| 2024-09-19 | `2400397661` | City note reports time-of-day signal settings adjusted. | Recorded operational adjustment. |
| 2025-07-14 | `2500272028` | Flashing-red complaint; City notes repairs completed. | Recorded complaint and maintenance response during July cluster. |
| 2025-07-14 | `2500272866` | Flashing-red complaint; City notes repairs completed. | Additional request; **do not** automatically treat as a distinct underlying fault. |
| 2026-04-07 | `2600113036` | Faded northbound crosswalk markings reported on S Wilcrest; selected by geographic screening. | Nearby candidate; exact affected crossing needs validation. |
| 2026-04-22 | `2600128932` | Complaint describes sidewalk damage restricting wheelchair access at Bissonnet/Wilcrest. | Citizen accessibility report; generic `Public Works` resolution does not prove repair. |
| 2026-05-01 | `2600140879` | Another wheelchair-accessibility concern at Bissonnet/Wilcrest. | Possible related concern; persistence or same defect unproven. |
| 2026-07-02 | `2600215977` | Southbound through-signal phase reportedly skips cycles. | Reported operational concern; not independently verified from request alone. |

Each case above is traceable by its exact case number to a row in the appropriate uploaded annual **311 candidate CSV**. The original City 311 archives are the primary raw source; candidate extracts are derivative evidence for local screening: https://houstontx.gov/311/servicerequestdata.html and https://311.houstontx.gov/servicerequestdata.html

**Data-quality rules to preserve:** (1) A duplicate service request is not a duplicate data row; preserve both and link parent service request numbers; (2) City `Service Completed` status is an administrative status, not automatic proof of physical repair; (3) address-validation notes can conflict with reported streets and map coordinates; (4) exclude nearby Boone Road, KIPP Way and other intersections from Wilcrest-specific counts unless a specific relation is demonstrated; (5) incident grouping needs manual audit before publication.

## 3. Roadway and Infrastructure Context

**As observed in 2019**, the RSA describes uneven and obstructed sidewalks, damaged curbs, some vehicle and pedestrian signal heads not properly aligned, one streetlight not functioning, dated traffic-signal hardware, bus-stop and crossing-placement issues, and school-related queuing. See the original *Location: Bissonnet at Wilcrest* section, report pp. 21–22. These are historical observations and must **not** be presented as current physical conditions without modern confirmation.

The City's September 2019 Safer Streets Update listed nine pedestrian/vehicle crashes in the preceding five years and recommended near-term signal maintenance and refreshed crosswalks and longer-term lighting, curb-ramp reconstruction, and crossing-management approaches. The slide does not supply injury severity.

**Important distinction:** Descriptions in the 2019 audit refer to the conditions observed at that time, not necessarily the intersection as it exists in 2026. A 2022 City grant application says short-term audit recommendations were implemented at twelve audited intersections; that is a City-reported claim, not independent verification of which specific elements at Wilcrest were completed. See the original application, source SRC-08.

## 4. Known Safety Interventions

### INT-001: Bissonnet Corridor Safe Streets

- **City identifier:** `N-100043` (project); benchmark WBS `N-100043-0001-3`.
- **Footprint:** Bissonnet between South Dairy Ashford and Hillcroft, encompassing Wilcrest intersection.
- **Administrative evidence:** 2022 application authorization and 2025 City/Council federal grant agreement; documented estimated total **$35,986,630.71** ($28,789,304.57 federal + $7,197,326.14 estimated local future match).
- **Design evidence:** The October 2024 design concept and *Appendix A Proposed Design Schematic* show existing versus proposed treatments at **Bissonnet/Wilcrest on PDF page 7**. Notably, the legend indicates an *existing signal to be replaced per City of Houston independently programmed projects*; the design sheet alone does not identify the separate project's contract or prove construction.
- **Project schedule evidence:** City's **2026-10-09 Construction Benchmark** lists project in design with a forecast construction NTP of **2029-01-03** and forecast final completion of **2030-03-24**. Dates are forecast, not actual milestones.
- **Construction completed at pilot intersection:** NOT VERIFIED.

Sources:
- https://houston.novusagenda.com/agendapublic/CoverSheet.aspx?ItemID=31342&MeetingID=763
- https://cipms.houstontx.gov/cc/cm/cons18m_bench_mark_eng.jsp
- Local user-uploaded 2024 schematic PDF: `d336089133f08de4031156c68feb3fff_Appendix_A_-_Proposed_Design_Schematic.pdf`, **PDF p. 7**. Published source: https://www.engagehouston.org/17318/widgets/76596/documents/69194

### INT-002: International Management District intersections

- **Identifiers:** City WBS `N-MD0320-0001-7`; TxDOT CSJ `0912-72-829`.
- **Footprint:** Four named intersections, including **Bissonnet/Wilcrest** (also Bellaire/Metro, Beechnut/Wilcrest, S Kirkwood/Stroud).
- **Planned scope:** Intersection and operational improvements including rehabilitating/reconstructing traffic signals, geometric layout, pavement markings, signage and lighting.
- **Administrative evidence:** August 2025 Council action on City–TxDOT Advance Funding Agreement. The Council background identifies a $2.5 million federal award and additional local-cost arrangements.
- **Construction completed at pilot intersection:** NOT VERIFIED.
- **Relationship to INT-001:** Both touch the same site. They remain separate project records until an explicit source establishes the exact dependency or scope overlap. The corridor drawing's independent-signal note may refer to this work, but is not conclusive.

Source: https://houston.novusagenda.com/agendapublic/CoverSheet.aspx?ItemID=35348&MeetingID=750

### Routine maintenance versus capital improvements

311 case-specific repair actions (e.g., breaker replacement or timer adjustment) are **operational maintenance**, not proof that either of the above capital projects has been constructed. A funded project, a conceptual schematic and a completed maintenance service call represent different classes of action.

### Status interpretation

- **Proposed/design:** A concept or drawing illustrates possible changes; it does not establish a built improvement.
- **Authorized/funded:** Government agreements or appropriations authorize work or funding; they are not construction-completion evidence.
- **Maintenance recorded:** A specific 311 technician note or work order can support work undertaken on that date, but not the completion of a separate capital project.
- **Completed construction:** Requires specific and dated completion evidence for the pertinent intervention or intersection, currently not available in this source set.

## 5. Evidence Timeline

The entries below are selected research anchors, not a comprehensive inventory of accepted infrastructure events. Administrative timelines and physical effects must be assessed separately.

| Date/period | Record type | Evidence | Limit or open question |
|---|---|---|---|
| 2019 | Road safety audit | FHWA/City examination of Bissonnet/Wilcrest identifies pedestrian-access and traffic-control concerns. | Historical observation only. |
| 2019-09 | City safety briefing | Nine pedestrian/vehicle crashes in prior five years reported in City presentation. | Different time/boundary than later CRIS query; severity not listed. |
| 2019-09 | Houston 311 | Several intersection-specific signal complaints. | Repeated requests do not prove repeated independent failures. |
| 2021 | Houston 311 | Reports on lighting above traffic signals and signal operations. | Physical outcome not consistently recorded. |
| 2022-08 to 2022-09 | Houston 311 / City technician notes | Breaker and power-supply replacements documented in selected cases. | Work on those visits, not proof of permanent resolution. |
| 2023-06 to 2023-08 | Houston 311 | Reports of faded intersection/crosswalk markings. | Records do not prove subsequent restriping. |
| 2024-10 | Corridor design | Proposed schematic shows Wilcrest treatments and separately programmed signal replacement notation. | Design, not completed construction; separate project identity unresolved. |
| 2025 | City approvals | Funding agreements support two separate projects covering the intersection. | Agreement does not prove construction. |
| 2026-04 to 2026-05 | Houston 311 | Wheelchair accessibility complaints at Bissonnet/Wilcrest. | Administrative case completion not physical repair verification. |
| 2026-09-11 | HPD public release | Reports pedestrian fatality near Bissonnet/Wilcrest. | Do not infer crash cause from complaint or audit history. |
| 2026-10-09 | City construction benchmark | Corridor project recorded as in design, with later construction forecasts. | Forecasts subject to change; no physical completion verified. |

### Cross-source issue themes

| Issue theme | Audit / historical record | 311 evidence | Intervention overlap | Current physical status |
|---|---|---|---|---|
| Signal operation and visibility | 2019 audit | Reports 2019–2026 and some technician repair notes | INT-001 design's separate signal note; INT-002 signal scope | Unverified |
| Sidewalks / wheelchair accessibility | 2019 audit sidewalk/curb issues | 2026 accessibility complaints | INT-001 corridor pedestrian-access intent | Unverified |
| Crosswalk markings | 2019 City recommendations | 2023 faded-markings and 2026 northbound markings reports | INT-002 pavement-marking scope; INT-001 proposals | Unverified |
| Street lighting | 2019 audit, one fixture nonworking at that time | 2021 reports of lights above signals out | INT-002 lighting scope | Unverified |
| Crash harm | CRIS query 2016–2026; HPD fatality release 2026 | Not a directly comparable 311 category | Safety rationale cited by City | Causation **not** established |

**Do not infer:** Same defect over seven years; unrepaired condition from a closed 311 case; government neglect; causal relationship between complaint/project and any specific collision; or confirmed project completion merely from authorization, design or funding.

## 6. Data Sources

Sources used or identified during the manual case investigation. External URLs link to the original publishers where available. The local derivative extracts are not substitutes for their raw sources. **Do not commit full raw 311 or CRIS exports by default**, and review possible personal information in narratives before publishing excerpts.

| Source ID | Origin | Exact source or local record | Evidence role |
|---|---|---|---|
| SRC-01 | TxDOT CRIS | User-exported `my_list (1).csv`, `CRIS Unit.csv`, `CRIS_person.csv`; data processed as of 2026-10-09 | Crash, unit, and person analysis; user-drawn polygon and filters preserved separately. |
| SRC-02 | City/FHWA | [2019 Road Safety Audit](https://houstontx.gov/visionzero/pdf/20190520-Houston%20RSA%20part%202-SR.pdf) | Historical road conditions and recommendations. |
| SRC-03 | Houston Public Works | [September 2019 Safer Streets Update](https://www.houstontx.gov/council/committees/tti/20190905/Safer-Streets-Update.pdf) | Historical crash summary and recommendations. |
| SRC-04 | Houston 311 | [Historical 311 data](https://311.houstontx.gov/servicerequestdata.html), annual public TXT exports 2019–2026 YTD | Raw complaint records. |
| SRC-05 | StreetSignal local analysis | Eight `streetsignal_311_candidates_...-YYYY.csv` derivative extracts produced by `research/extract_311_candidates.py` | Reproducible initial screening; **not** verified event counts. |
| SRC-06 | Houston Police Department | [September 11, 2026 pedestrian fatality release](https://www.houstontx.gov/police/nr/2026/sep/nr091126-5.htm) | Separate contemporaneous incident account. |
| SRC-07 | City Council | [Bissonnet corridor grant agreement](https://houston.novusagenda.com/agendapublic/CoverSheet.aspx?ItemID=31342&MeetingID=763) | Corridor grant and authorization. |
| SRC-08 | City of Houston | [2022 Bissonnet Safe Streets federal grant application](https://ehq-production-us-california.s3.us-west-1.amazonaws.com/38ff3241df3dd90a1d6badfd41db0f26c16a69ed/original/1663877550/f22fd953c32388a78deb422b607f0371_Bissonnet_Safe_Streets_and_Roads_for_All_Application-NARRATIVE.pdf) | Original safety rationale and City's historical implementation statements. |
| SRC-09 | City of Houston / Engage Houston | [October 2024 Appendix A proposed schematic](https://www.engagehouston.org/17318/widgets/76596/documents/69194), **PDF page 7** | Proposed Wilcrest layout and independent signal replacement note. |
| SRC-10 | City Council | [International Management District funding agreement](https://houston.novusagenda.com/agendapublic/CoverSheet.aspx?ItemID=35348&MeetingID=750) | Separately authorized intersection improvements; scope, IDs. |
| SRC-11 | Houston Public Works | [Construction benchmark](https://cipms.houstontx.gov/cc/cm/cons18m_bench_mark_eng.jsp), checked 2026-10-09 | Corridor design status and forecast milestones; dynamic source. |
| SRC-12 | City of Houston / Engage Houston | [October 2024 Design Concept Report](https://www.engagehouston.org/17318/widgets/76596/documents/69193) | Context for proposed roadway design; individual final design not independently certified. |

**Case-file provenance requirements:** Record extraction/retrieval timestamp, public URL, report/document date, source identifiers, query boundary, original complaint text (in the controlled working data), and checksum for each source actually ingested. Some of these metadata fields have not yet been captured, so treat them as implementation requirements, not completed facts.

## 7. Data Limitations

1. **Spatial attribution:** The 246 CRIS crashes came from a small user-drawn polygon. `INTERSECTION`, `INTERSECTION RELATED`, `NON INTERSECTION`, and `DRIVEWAY ACCESS` are distinct original categories. Do not rename all 246 as intersection collisions.
2. **Geocoding:** Multiple CRIS cases share identical coordinates; 311 validated addresses can differ from citizen-specified intersections. Use the narrative and location evidence, not proximity alone.
3. **Request duplication:** 311 duplicates, merges, and parent cases can represent many public reports concerning one condition. Preserve case IDs and relationships; do not arbitrarily collapse or multiply events.
4. **Case closure:** `Service Completed`, `Merged`, or other administrative state does not by itself establish physical repair. Technician notes with specific actions support only what those notes actually say.
5. **Temporal completeness:** Candidate date minima and maxima do not establish full archive coverage; the 2026 YTD subset is not directly comparable to completed years.
6. **2021 versions:** The separate July–December 2021 export and full-year 2021 export overlap, and certain timestamps or notes differ. The 179 full-year candidates are the baseline; do not add the earlier 92 candidates again.
7. **Project attribution:** The corridor project's independently programmed signal notation is not yet definitively linked to the separately funded International Management District project.
8. **Evidence timing:** Historical observations, current complaints, proposed works and construction forecasts refer to different time periods and cannot be treated as a current engineering inspection.
9. **Causal claims:** There is no demonstrated causal link from the 311 complaints or proposed works to any individual TxDOT/HPD crash.
10. **Privacy and provenance:** Some raw request texts may contain identifying contact details; keep full raw files out of public GitHub by default and publish curated, source-attributed excerpts only after review.

## 8. Preliminary Findings

**Supported by the present source inventory:** There is documented traffic harm within the pilot's preliminary search polygon, repeated public complaints about signal operation and pedestrian infrastructure at or near Bissonnet/Wilcrest across several years, documented City maintenance actions on certain dates, historical City/FHWA safety recommendations, and two different government-funded projects that include the intersection.

**Not yet supported:** That a particular defect persisted continuously from 2019 to 2026; that a documented complaint caused a crash; that a 311 closure means permanent repair; or that either capital project's intersection-specific construction has been completed.

**Research stage:** Initial data gathering and intervention inventory complete for v0.1; claim-by-claim location adjudication, cross-record incident grouping, and ongoing source updates remain open. Treat this as an **engineering baseline and research draft**, not as a final public-facing certification.

### Application implementation handoff (proposed, not built)

### Suitable as versioned *source inputs* now

- CRIS exported crash, unit and person CSVs with full query metadata and source date.
- Eight Houston 311 *candidate* extracts, with year, case ID, both location fields and narrative notes preserved.
- May 2019 FHWA Road Safety Audit and September 2019 City recommendations.
- City Council project agreements, October 2024 schematic and dated construction forecasts.
- HPD fatality news release as a separate source with its own location wording.

### Still required before public-facing conclusions

1. **Location adjudication:** Tag each proposed 311 claim `intersection_specific`, `nearby`, `conflicting_location`, or `undetermined`, preserving why.
2. **Incident relationships:** Group duplicate, merged or parent-linked service requests without deleting individual report rows. Avoid dividing raw count by an arbitrary factor.
3. **Source-led claim validation:** Every sentence in final case needs a direct source ID / document page or case ID, a time period, and a confidence/limitation statement.
4. **Project-status check:** Document which official source supports `authorized`, `design`, `construction_started`, or `completed`; do not advance status through inference.
5. **Completeness:** Verify date and schema coverage for raw annual archives; preliminary candidate dates alone cannot establish source completeness.

### First application data contracts (proposed, not yet implemented)

`Case` (location, aliases, review boundary, review version) → `Source` (URL or raw file, publication/extract date, retrieval date, hash) → `EvidenceRecord` (source primary key, time, raw location, normalized location, type, status, notes) → `Relationship` (duplicates, same work order, thematic, geographically overlapping) → `Claim` (plain-language statement, evidence IDs, uncertainty, verification status).

**First deterministic acceptance test:** For Bissonnet/Wilcrest, the processing tool must ingest the eight candidate extracts; report **1,437 screened records** (not 1,437 confirmed incidents); preserve source case IDs and full original notes; keep the overlapping 2021 files out of duplicate annual totals; and never label a capital project or complaint automatically 'completed' just because an administrative case is closed.

### Baseline versioning policy

This document is a **frozen baseline draft for engineering and case review**, not a claim that physical conditions are frozen or that research cannot be corrected. Each public record may have a separate observation date, publication date and extraction date. New evidence should amend a documented source entry, not silently overwrite the old one. Version and correct this file after review; commit it to GitHub only when the initial claims, schema and privacy/provenance decisions have been checked.
