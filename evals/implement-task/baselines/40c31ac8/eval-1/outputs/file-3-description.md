# File 3: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and aggregates their severity counts.

## Sibling Reference

Follows the pattern established by the existing `fetch` and `list` methods in the same file:
- Method signature: `pub async fn method_name(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Error handling: uses `.context()` wrapping for all fallible operations
- Database access: uses SeaORM queries

## Detailed Changes

Add a new method to the `impl AdvisoryService` block:

```rust
/// Compute severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts defaulting to zero for levels
/// with no advisories.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // First verify the SBOM exists, returning 404 if not found
    // (follows the pattern from fetch() for existence checks)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM {sbom_id} not found")))
        .context("Fetching SBOM for severity summary")?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    // Using the entity::sbom_advisory module for the join
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("Querying SBOM advisories")?;

    // Deduplicate by advisory ID using a HashSet
    let unique_advisory_ids: HashSet<_> = advisories
        .iter()
        .map(|sa| sa.advisory_id.clone())
        .collect();

    // Fetch the full advisory details for each unique advisory to get severity
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        if let Some(advisory) = self
            .fetch(advisory_id.clone(), tx)
            .await?
        {
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- not counted in named buckets
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Required Imports

Add to the file's import section:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Convention Conformance

- Method signature follows the existing `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern from `fetch` and `list`
- Error handling uses `.context()` wrapping matching the established pattern
- SBOM existence check returns 404 for non-existent IDs (acceptance criterion #2)
- Deduplication via `HashSet` ensures unique advisory counts (acceptance criterion #3)
- `SeveritySummary::default()` ensures all zeros when no advisories exist (acceptance criterion #4)
- Uses the `sbom_advisory` join table as specified in Implementation Notes
- Leverages the existing `fetch` method on `AdvisoryService` to get advisory details including severity

## Notes

- The exact SeaORM query syntax and entity module paths would be confirmed by reading the actual source files with Serena before implementing. The above is a structural illustration following the patterns described in the task.
- If a more efficient SQL-level aggregation (e.g., `GROUP BY severity`) is possible via SeaORM, that would be preferred for the performance criterion (under 200ms for 500 advisories). The individual-fetch approach above is shown for clarity but would be replaced with a single aggregation query in the actual implementation.
