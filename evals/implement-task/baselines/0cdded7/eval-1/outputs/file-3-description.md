# File 3: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Action: MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries advisories linked to a given SBOM and aggregates their severity counts.

## Detailed Changes

Add a new method to the `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
/// Compute aggregated severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<Option<SeveritySummary>, anyhow::Error> {
    // First, verify the SBOM exists. If not, return None (caller maps to 404).
    let sbom_exists = sbom::Entity::find_by_id(sbom_id)
        .one(self.db.connection(tx))
        .await
        .context("failed to check SBOM existence")?;

    if sbom_exists.is_none() {
        return Ok(None);
    }

    // Query advisories linked to this SBOM via the sbom_advisory join table.
    // Use DISTINCT to deduplicate by advisory ID.
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(advisory::Entity)
        .all(self.db.connection(tx))
        .await
        .context("failed to fetch advisories for SBOM severity summary")?;

    // Deduplicate by advisory ID and count by severity level.
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory) in advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id) {
                match adv.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown severity levels are not counted in specific buckets
                }
                summary.total += 1;
            }
        }
    }

    Ok(Some(summary))
}
```

## Required Imports (added at the top of the file)

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

Also ensure these entity imports exist (they likely already do given existing methods):
```rust
use entity::{advisory, sbom, sbom_advisory};
```

## Conventions Applied

- **Method signature**: Matches existing `fetch` and `list` methods -- takes `&self`, entity ID, and `&Transactional<'_>`, returns `Result<Option<T>, anyhow::Error>`
- **Return `Option`**: Returns `None` when the SBOM does not exist, allowing the endpoint handler to map this to a 404. This matches the pattern in the `fetch` method.
- **`.context()` wrapping**: All database operations use `.context("descriptive message")` for meaningful error messages, matching the established error handling pattern from `common/src/error.rs`
- **Database access**: Uses `self.db.connection(tx)` for transactional database access, matching existing service methods
- **SeaORM patterns**: Uses `Entity::find()`, `.filter()`, `.find_also_related()`, `.all()` -- consistent with existing query patterns in the service
- **Deduplication**: Uses `HashSet` to deduplicate by advisory ID, satisfying the acceptance criterion "counts only unique advisories"
- **Case handling**: Matches both capitalized and lowercase severity strings for robustness
