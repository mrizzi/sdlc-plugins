## Repository
trustify-backend

## Description
Add a severity aggregation method to `SbomService` that queries the database for advisory severity counts linked to a given SBOM. The method joins the `sbom_advisory` join table with the `advisory` table, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary`. It must also support an optional severity threshold parameter to filter counts above a given severity level. The method should return a 404-equivalent error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary` method to SbomService

## API Changes
- `SbomService::get_advisory_severity_summary(sbom_id, threshold: Option<SeverityThreshold>)` — NEW: returns `Result<AdvisorySeveritySummary, AppError>`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest). Each method takes a database connection/transaction, uses SeaORM query builders, and returns `Result<T, AppError>` with `.context()` wrapping for error handling.
- Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` as the join table between SBOMs and advisories. Join to `entity/src/advisory.rs` to access the severity field.
- Use SeaORM's `select_only()`, `column()`, and `group_by()` to build the aggregation query. Count distinct advisory IDs to ensure deduplication per the feature requirements.
- Use the shared query builder helpers in `common/src/db/query.rs` if applicable for filtering.
- Validate that the SBOM exists before running the aggregation query. Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist, consistent with existing SBOM endpoints.
- When the optional `threshold` parameter is provided, filter the query to only include advisories at or above the given severity level. Define a severity ordering: Critical > High > Medium > Low.
- No new database tables are required per non-functional requirements — use only existing `sbom_advisory` and `advisory` entity relationships.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend; follow its method signature patterns (db connection parameter, Result return type)
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse where applicable for the severity filter
- `common/src/error.rs::AppError` — error enum for returning 404 when SBOM is not found
- `entity/src/sbom_advisory.rs` — join table entity for SBOM-to-Advisory relationship
- `entity/src/advisory.rs` — advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService` has a `get_advisory_severity_summary` method that returns `AdvisorySeveritySummary`
- [ ] The method deduplicates advisories by advisory ID before counting
- [ ] The method groups counts by severity level (critical, high, medium, low) and computes total
- [ ] The method returns an appropriate error when the SBOM ID does not exist
- [ ] When a threshold parameter is provided, only severity levels at or above the threshold are included in the counts
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit/service test: given an SBOM with known advisories at various severities, verify the returned counts are correct
- [ ] Unit/service test: given duplicate advisory links (same advisory linked multiple times), verify deduplication produces correct counts
- [ ] Unit/service test: given a non-existent SBOM ID, verify the method returns a not-found error
- [ ] Unit/service test: given a threshold of "high", verify only critical and high counts are returned (medium and low are zero or omitted)

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
