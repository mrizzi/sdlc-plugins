# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries the `sbom_advisory` join table, joins to the advisory entity to get severity levels, deduplicates by advisory ID, and aggregates counts per severity level.

## Detailed Changes

### Change: Add `severity_summary` method to `AdvisoryService` impl block

**Location**: Inside the `impl AdvisoryService` block, after the existing `list` method.

**Code to add**:

```rust
/// Computes aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts advisories at each
/// severity level (Critical, High, Medium, Low).
///
/// Returns a `SeveritySummary` with per-level counts and a total. All counts
/// default to 0 when no advisories exist at a given severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404-mapped error if not found
    // (follow the pattern used by fetch() for existence checks)

    // Query sbom_advisory join table filtered by sbom_id
    // Join to advisory entity to access the severity field
    // Use DISTINCT on advisory ID to deduplicate
    // Group by severity level and count

    // Map query results to SeveritySummary struct
    let mut summary = SeveritySummary::default();
    // For each (severity, count) row:
    //   match severity:
    //     "Critical" => summary.critical = count,
    //     "High" => summary.high = count,
    //     "Medium" => summary.medium = count,
    //     "Low" => summary.low = count,
    // summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Required imports to add at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Conventions Applied

- **Method signature**: Follows the same `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern as `fetch` and `list` methods.
- **Error handling**: Uses `.context()` wrapping on database operations, matching sibling methods.
- **SBOM existence check**: Verifies SBOM exists before querying, returning an error that maps to HTTP 404, consistent with existing SBOM endpoints.
- **Deduplication**: Uses DISTINCT on advisory ID in the query to satisfy the "counts only unique advisories" acceptance criterion.
- **Default values**: Uses `SeveritySummary::default()` to initialize all counts to 0, ensuring missing severity levels return 0.
- **Documentation**: Doc comment on the method explaining behavior, parameters, and return value.

## Implementation Notes

- The `sbom_advisory` join table entity is at `entity/src/sbom_advisory.rs` -- would use this for the SeaORM query.
- The `AdvisorySummary` struct in `advisory/model/summary.rs` has a `severity` field -- this is the source of the severity level for each advisory.
- The method uses a single query with GROUP BY to aggregate counts, avoiding N+1 query patterns for performance (acceptance criterion: under 200ms for 500 advisories).
