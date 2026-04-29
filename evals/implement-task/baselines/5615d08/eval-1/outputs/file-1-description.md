# File 1: `modules/fundamental/src/advisory/service/advisory.rs`

**Action**: Modify (add method)

## What Changes

Add a `severity_summary` method to the existing `AdvisoryService` struct. This method aggregates advisory severity counts for a given SBOM by querying the `sbom_advisory` join table.

## Detailed Changes

### New method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, following the pattern of the existing `fetch` and `list` methods:

```rust
/// Returns aggregated advisory severity counts for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts for critical, high, medium, low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let sbom = self.sbom_service.fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("failed to query sbom_advisory table")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch advisory summaries and count by severity
    let mut critical: u64 = 0;
    let mut high: u64 = 0;
    let mut medium: u64 = 0;
    let mut low: u64 = 0;

    for advisory_id in &unique_advisory_ids {
        if let Some(advisory) = self.fetch(advisory_id.clone(), tx).await? {
            match advisory.severity.as_deref() {
                Some("critical") | Some("Critical") => critical += 1,
                Some("high") | Some("High") => high += 1,
                Some("medium") | Some("Medium") => medium += 1,
                Some("low") | Some("Low") => low += 1,
                _ => {} // Unknown or None severity -- not counted
            }
        }
    }

    let total = critical + high + medium + low;

    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

### New imports needed at the top of the file

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Patterns Followed

- Same method signature pattern as `fetch` and `list`: `&self`, entity ID, `&Transactional<'_>`
- Error wrapping with `.context()` matching `common/src/error.rs` pattern
- Returns `Result<T, AppError>` consistent with all service methods
- 404 handling for non-existent SBOM, consistent with existing SBOM endpoints
