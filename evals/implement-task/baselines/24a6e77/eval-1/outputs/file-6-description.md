# File 6: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries advisories linked to a given SBOM and aggregates counts by severity level.

## Detailed Changes

Add the following method to the `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
/// Returns aggregated severity counts for all advisories linked to the
/// specified SBOM. Deduplicates advisories by advisory ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404 if not found
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("fetching SBOM for severity summary")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // 2. Query advisories linked to this SBOM via the sbom_advisory join table
    //    Use DISTINCT on advisory ID to deduplicate
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("querying advisories for SBOM")?;

    // 3. Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id.clone()) {
                match advisory.severity.as_deref() {
                    Some("Critical") => summary.critical += 1,
                    Some("High") => summary.high += 1,
                    Some("Medium") => summary.medium += 1,
                    Some("Low") => summary.low += 1,
                    _ => {} // Unknown or None severity — do not count
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

Also add the necessary import at the top of the file:

```diff
+use crate::advisory::model::severity_summary::SeveritySummary;
+use std::collections::HashSet;
```

## Conventions Applied

- **Method signature**: Matches the existing `fetch` and `list` methods — takes `&self`, an `Id` parameter, and `&Transactional<'_>` for database access.
- **Return type**: Returns `Result<SeveritySummary, AppError>`, following the project-wide error handling convention.
- **Error propagation**: Uses `.context("descriptive message")` for all fallible operations, wrapping errors into `AppError` as established in `common/src/error.rs`.
- **404 handling**: Returns `AppError::not_found(...)` when the SBOM does not exist, consistent with how existing SBOM endpoints handle missing resources.
- **Deduplication**: Uses a `HashSet` to track seen advisory IDs, satisfying the acceptance criterion for deduplicating advisory links.
- **Default values**: `SeveritySummary::default()` initializes all counts to 0, satisfying the acceptance criterion that all severity levels default to 0.
