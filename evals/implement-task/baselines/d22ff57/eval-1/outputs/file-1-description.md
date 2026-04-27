# File 1: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Summary

Add a `severity_summary` method to the existing `AdvisoryService` struct, following the
same pattern used by the existing `fetch` and `list` methods.

## Detailed Changes

### Add `severity_summary` method to `AdvisoryService` impl block

Insert a new method after the existing `list` (or `search`) method:

```rust
/// Returns a severity count summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, and Low,
/// plus a total count.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    //    Use sbom entity lookup, similar to how fetch verifies entity existence
    let _sbom = entity::sbom::Entity::find_by_id(sbom_id)
        .one(&self.db(tx))
        .await
        .context("failed to query SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {sbom_id} not found")))?;

    // 2. Query sbom_advisory join table for all advisories linked to this SBOM
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(&self.db(tx))
        .await
        .context("failed to query SBOM advisories")?;

    // 3. Collect unique advisory IDs to avoid double-counting
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id)
        .collect();

    // 4. Fetch AdvisorySummary for each unique advisory
    //    (batch query rather than N+1)
    let advisories = entity::advisory::Entity::find()
        .filter(entity::advisory::Column::Id.is_in(unique_advisory_ids.iter().cloned()))
        .all(&self.db(tx))
        .await
        .context("failed to fetch advisory details")?;

    // 5. Count by severity level
    let mut summary = SeveritySummary::default();
    for advisory in &advisories {
        match advisory.severity.as_deref() {
            Some("Critical") | Some("critical") => summary.critical += 1,
            Some("High") | Some("high") => summary.high += 1,
            Some("Medium") | Some("medium") => summary.medium += 1,
            Some("Low") | Some("low") => summary.low += 1,
            _ => {} // Unknown or None severity -- not counted in any bucket
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Add required imports

At the top of the file, add:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Conventions Applied

- **Method signature:** Follows the `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern from `fetch` and `list`.
- **Error handling:** Uses `.context()` wrapping on all fallible operations, matching the existing pattern.
- **404 handling:** Checks SBOM existence and returns `AppError::not_found` consistent with existing endpoints.
- **Documentation:** Doc comment added explaining purpose, parameters, and behavior.
- **Deduplication:** Uses `HashSet` to collect unique advisory IDs before counting, satisfying the acceptance criterion.
- **Batch query:** Avoids N+1 by using `is_in()` filter for batch advisory lookup.
