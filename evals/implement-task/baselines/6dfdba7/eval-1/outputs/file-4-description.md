# File 4: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and aggregates their severity counts.

## Conventions Applied

- Follows the method signature pattern of existing `fetch` and `list` methods: `pub async fn method(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.
- Uses `.context()` wrapping for error propagation.
- Queries via SeaORM entity relationships.
- Deduplicates by advisory ID to satisfy the acceptance criterion.

## Detailed Changes

Add the following method to the `impl AdvisoryService` block, after the existing `list` and `fetch` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High,
/// Medium, Low) and a total count. Advisories are deduplicated by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404-compatible error if not
    let _sbom = self
        .db
        .find_by_id::<sbom::Entity>(sbom_id.clone())
        .one(tx.connection())
        .await
        .context("Failed to query SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // 2. Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .find_also_related(advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // 3. Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_link, advisory_opt) in advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id.clone()) {
                // Map the advisory's severity to the corresponding counter
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => { /* Unknown or missing severity -- not counted in named buckets */ }
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Additional Imports Required

Add at the top of the file (if not already present):

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use trustify_entity::{sbom, sbom_advisory, advisory};
use std::collections::HashSet;
```

## Notes

- The severity field mapping (`"Critical"`, `"High"`, etc.) follows the pattern from `AdvisorySummary` in `model/summary.rs` which has a `severity` field. The exact string values would be confirmed by inspecting the `advisory` entity definition and existing data.
- The SBOM existence check ensures a 404 is returned for non-existent SBOM IDs, matching the behavior of existing SBOM endpoints.
- Deduplication uses a `HashSet` on advisory ID to handle duplicate join table entries.
- The `total` field counts all unique advisories regardless of severity, including those with unknown/missing severity values. This ensures `total` always equals the number of unique advisories.
- An alternative implementation could use a SQL `GROUP BY` query for better performance with large advisory sets. The in-memory approach is chosen for clarity and consistency with the existing service patterns, but a SQL-level optimization could be applied if performance testing shows it's needed (the acceptance criterion requires under 200ms for up to 500 advisories).
