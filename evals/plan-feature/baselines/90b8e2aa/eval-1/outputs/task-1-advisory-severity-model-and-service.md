## Repository
trustify-backend

## Target Branch
main

## Description
Add the advisory severity summary response model and aggregation service method. This creates the data layer for the new advisory-summary endpoint: a response struct `AdvisorySeveritySummary` that holds severity counts (critical, high, medium, low, total), and a service method on `SbomService` that queries the `sbom_advisory` join table to aggregate unique advisory counts grouped by severity for a given SBOM ID.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with fields: critical, high, medium, low, total (all u64); derives Serialize, Deserialize, Debug, Clone, PartialEq

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries the sbom_advisory join table, joins with the advisory table to get severity, deduplicates by advisory ID, and groups counts by severity level

## Implementation Notes
- The aggregation query must deduplicate advisories by advisory ID before counting — the same advisory may be linked to an SBOM through multiple paths (e.g., via different packages). Use `SELECT DISTINCT advisory_id` or a `GROUP BY advisory_id` to ensure each advisory is counted exactly once.
- The severity field is on the `AdvisorySummary` struct (see `modules/fundamental/src/advisory/model/summary.rs`). Use the same severity enum/type for consistency.
- Use SeaORM's `select` with raw SQL or query builder to perform the `COUNT ... GROUP BY severity` aggregation. Refer to existing query patterns in `common/src/db/query.rs`.
- The method should return an error (which maps to 404 via AppError) if the SBOM ID does not exist. Check for SBOM existence before running the aggregation query, consistent with the pattern in the existing `get` method in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error Handling: wrap all fallible operations with `.context()` to produce descriptive error messages. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's .rs service file scope.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure for new domain code. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's model/ directory scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reuse the same severity type/enum for consistency in the aggregation query
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table SeaORM entity; use this entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity data; join with sbom_advisory for severity counts
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reference for building the aggregation query
- `common/src/error.rs::AppError` — error enum that implements IntoResponse; use for SBOM-not-found error case

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical, high, medium, low, total (all numeric)
- [ ] `SbomService::advisory_severity_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Method returns an appropriate error when the SBOM ID does not exist
- [ ] Severity categories match the existing severity definitions in the advisory model

## Test Requirements
- [ ] Unit test: aggregation method returns correct counts for an SBOM with advisories at multiple severity levels
- [ ] Unit test: aggregation method deduplicates advisories linked multiple times to the same SBOM
- [ ] Unit test: aggregation method returns all-zero counts for an SBOM with no advisories
- [ ] Unit test: aggregation method returns error for a non-existent SBOM ID

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental` — all existing and new tests pass

## Dependencies
- None

---
[sdlc-workflow] Description digest: sha256-md:865365c54437974f938fee497fde6ce9f14fefef1ce3bcb2f01b0c86ebd77965
