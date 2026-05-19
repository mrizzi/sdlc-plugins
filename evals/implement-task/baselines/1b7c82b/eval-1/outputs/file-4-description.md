# File 4: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService`. This method queries the `sbom_advisory` join table to find all advisories linked to a given SBOM, deduplicates by advisory ID, reads each advisory's severity from `AdvisorySummary`, counts by severity level, and returns a `SeveritySummary` struct.

## Detailed Changes

### New Method: `severity_summary`

Add the following method to the `AdvisoryService` impl block, following the pattern of existing `fetch` and `list` methods:

```rust
/// Retrieves an aggregated severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts advisories at each severity level
/// (Critical, High, Medium, Low). Returns a `SeveritySummary` with per-level counts
/// and a total.
///
/// Returns `AppError` with 404 status if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (Follow the pattern used by existing SBOM endpoints for 404 handling)

    // Query sbom_advisory join table for all advisories linked to this SBOM
    // Use entity::sbom_advisory to perform the join
    // Deduplicate by advisory ID (using DISTINCT or a HashSet)

    // For each unique advisory, read its severity from AdvisorySummary
    // Count by severity level: Critical, High, Medium, Low

    // Build and return SeveritySummary with counts and total
    let mut summary = SeveritySummary::default();

    // ... query logic using SeaORM ...
    // For each advisory linked to the SBOM:
    //   match severity {
    //       "Critical" => summary.critical += 1,
    //       "High" => summary.high += 1,
    //       "Medium" => summary.medium += 1,
    //       "Low" => summary.low += 1,
    //       _ => {} // unknown severity levels are not counted
    //   }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Implementation Details

1. **SBOM existence check**: Before querying advisories, verify the SBOM exists. If not, return an `AppError` that maps to HTTP 404, consistent with existing SBOM endpoints.

2. **Query approach**: Use SeaORM to query `entity::sbom_advisory` filtered by `sbom_id`, join to advisory entity to get advisory details, then use the `severity` field from `AdvisorySummary` (in `modules/fundamental/src/advisory/model/summary.rs`).

3. **Deduplication**: Use `DISTINCT` on advisory ID in the SQL query (via SeaORM's query builder) to ensure each advisory is counted only once, even if linked multiple times in the join table.

4. **Severity level counting**: Match on the severity string from `AdvisorySummary.severity` field. Only count known severity levels (Critical, High, Medium, Low). Unknown levels are silently skipped.

5. **Total calculation**: Sum of all four severity-level counts, ensuring consistency.

### Conventions Applied

- Method signature follows existing `fetch`/`list` pattern: `&self, id: Id, tx: &Transactional<'_>`
- Return type uses `Result<T, AppError>` with `.context()` wrapping for error messages
- Uses SeaORM entities from `entity/src/` for database queries
- Doc comment on the method describes purpose, behavior, and error conditions
- Placed alongside existing methods in the same impl block
