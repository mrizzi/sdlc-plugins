# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and aggregates their severity counts.

## Detailed Changes

Add the following method to the existing `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High,
/// Medium, Low) and a total. Deduplicates advisories by ID before counting.
///
/// Returns `AppError` (404) if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Uuid,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found.
    let _sbom = entity::sbom::Entity::find_by_id(sbom_id)
        .one(self.db.connection(tx))
        .await
        .context("Failed to query SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table.
    // Use DISTINCT on advisory ID to deduplicate.
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(self.db.connection(tx))
        .await
        .context("Failed to query advisories for SBOM")?;

    // Deduplicate by advisory ID and aggregate severity counts.
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id) {
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or null severity -- skip
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

Also add the necessary import at the top of the file (if not already present):

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Conventions Applied

- **Method signature**: Follows the existing `fetch` and `list` pattern -- takes `&self`, the identifier, and `tx: &Transactional<'_>`.
- **Error handling**: Uses `.context()` wrapping on all database operations and `?` propagation, matching sibling methods.
- **404 handling**: Checks SBOM existence first and returns `AppError::not_found()` if missing, consistent with how existing SBOM endpoints handle missing resources.
- **Deduplication**: Uses a `HashSet` of advisory IDs to ensure each advisory is counted only once, even if the join table has duplicate entries.
- **Default values**: `SeveritySummary::default()` initializes all counts to 0, satisfying the acceptance criterion.
- **Case handling**: Matches severity strings case-insensitively (both "Critical" and "critical") for robustness, though the actual codebase may have a consistent casing convention.

## Alternative Approach Considered

A SQL-level `GROUP BY severity COUNT(DISTINCT advisory_id)` query would be more performant for very large datasets. However, the in-memory approach matches the existing pattern of fetching entities and processing in Rust, and the acceptance criteria specify performance requirements only up to 500 advisories, which is well within in-memory processing limits. If profiling shows this is a bottleneck, a raw SQL query could replace the SeaORM approach.
