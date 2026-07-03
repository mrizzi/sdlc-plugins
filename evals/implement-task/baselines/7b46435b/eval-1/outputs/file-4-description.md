# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that aggregates advisory severity
counts for a given SBOM by querying the `sbom_advisory` join table and the `advisory`
table.

## Detailed Changes

### Add imports (at the top of the file, with existing imports)

Add imports for the new model and any required collection types:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### Add method to `impl AdvisoryService` block

Insert the `severity_summary` method into the existing `impl AdvisoryService` block,
after the existing `fetch` and `list` methods, following their pattern:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and returns counts per severity
/// level (Critical, High, Medium, Low) along with a total count.
///
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (Follow the pattern used by existing fetch methods that validate entity existence)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id, tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM with id {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table,
    // joining with the advisory table to get severity information.
    // Use DISTINCT on advisory ID to deduplicate (acceptance criterion #3).
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Deduplicate by advisory ID using a HashSet
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory) in advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id) {
                // Count by severity level using the severity field from AdvisorySummary
                match adv.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {} // Unknown or missing severity levels are not counted in named buckets
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Conventions Applied

- **Method signature**: Follows the same pattern as `fetch` and `list` -- takes `&self`, domain-specific ID parameter, and `tx: &Transactional<'_>`.
- **Return type**: `Result<SeveritySummary, AppError>` matching sibling methods.
- **Error handling**: Uses `.context()` wrapping on fallible operations, matching the project's error handling convention.
- **404 handling**: Validates SBOM existence before proceeding, returning a descriptive error message, consistent with existing SBOM endpoint behavior.
- **Transaction context**: Passes `tx` through to database operations, following the transactional pattern used throughout the service layer.
- **Documentation**: Method has a comprehensive `///` doc comment explaining purpose, behavior, and error cases.
- **Naming**: `severity_summary` follows the `verb_noun` / `adjective_noun` pattern used by other service methods.

## Notes

- The SBOM existence check ensures the 404 acceptance criterion is met. Without it, a non-existent SBOM would return an empty summary (all zeros) rather than a 404 error.
- Deduplication uses a `HashSet<Id>` to track seen advisory IDs, ensuring each advisory is counted exactly once even if multiple join table entries exist.
- The `total` field counts all unique advisories regardless of severity level, including those with unknown or missing severity values (which are not counted in the named severity buckets but do contribute to the total).
- Performance: For SBOMs with up to 500 advisories, this single-query approach with in-memory deduplication and counting should comfortably meet the 200ms response time requirement. An alternative approach using a SQL `COUNT(DISTINCT ...) GROUP BY severity` query would be more efficient for very large advisory counts, but the in-memory approach is simpler and consistent with patterns in the codebase.
