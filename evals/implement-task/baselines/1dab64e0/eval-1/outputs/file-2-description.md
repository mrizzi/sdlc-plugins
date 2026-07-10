# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates vulnerability advisory severity counts for a given SBOM.

## Pre-change Inspection

Before modifying, inspect the file using:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")
```

Then read the specific method signatures:
```
mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)
mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)
```

Also inspect the join table entity:
```
mcp__serena_backend__find_symbol("sbom_advisory", include_body=true)
```

And the severity field on AdvisorySummary:
```
mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)
```

## Changes

Add a new method `severity_summary` to the `impl AdvisoryService` block. The method follows the same pattern as `fetch` and `list`:

```rust
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM ID, deduplicates by advisory ID, and counts each severity level
/// (Critical, High, Medium, Low). Returns a `SeveritySummary` with per-level counts
/// and a total.
///
/// Returns `AppError::NotFound` if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists -- return 404 if not found
    //    (Use SbomService::fetch or a direct entity lookup to confirm existence)
    //    This matches the existing pattern where endpoints return 404 for non-existent entities.

    // 2. Query sbom_advisory join table for all advisories linked to this SBOM
    //    Use SeaORM query builder:
    //    entity::sbom_advisory::Entity::find()
    //        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
    //        .all(tx)

    // 3. Collect unique advisory IDs (deduplicate)
    //    Use a HashSet<Id> to ensure each advisory is counted only once.

    // 4. For each unique advisory, fetch its severity from AdvisorySummary
    //    Or perform a JOIN query that fetches advisory severity in one query:
    //    SELECT DISTINCT a.id, a.severity FROM advisory a
    //    INNER JOIN sbom_advisory sa ON sa.advisory_id = a.id
    //    WHERE sa.sbom_id = $1

    // 5. Count by severity level
    //    Initialize counters: critical=0, high=0, medium=0, low=0
    //    Iterate over advisory severities and increment appropriate counter.

    // 6. Compute total = critical + high + medium + low

    // 7. Return SeveritySummary { critical, high, medium, low, total }
}
```

## Key Design Decisions

1. **SBOM existence check first**: Matches the existing pattern where endpoints return 404 for non-existent entities rather than returning empty results. Checked by verifying the `sbom` entity exists before querying advisories.

2. **Deduplication**: The `sbom_advisory` join table may have multiple rows linking the same advisory to an SBOM (e.g., through different vulnerability paths). Use `DISTINCT` in SQL or `HashSet` in Rust to count each advisory only once.

3. **Single query approach**: For performance (< 200ms for 500 advisories), prefer a single SQL query with `GROUP BY severity` and `COUNT(DISTINCT advisory_id)` rather than fetching all advisories and counting in application code.

4. **Error handling**: Wrapping with `.context("Failed to fetch severity summary for SBOM")` matching the existing pattern in `common/src/error.rs`.

## Imports to Add

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;  // Only if deduplication is done in Rust rather than SQL
```
