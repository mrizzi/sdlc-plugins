# File 4: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

### Add import for the new model

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Add `severity_summary` method to `AdvisoryService` impl block

Insert the following method into the existing `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts occurrences per
/// severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = entity::sbom::Entity::find_by_id(&sbom_id)
        .one(tx.connection())
        .await
        .context("Failed to query SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Find all advisories linked to this SBOM via the join table
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(&sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisory links")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch each unique advisory and count by severity
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        let advisory = entity::advisory::Entity::find_by_id(advisory_id)
            .one(tx.connection())
            .await
            .context("Failed to fetch advisory for severity aggregation")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or null severity -- not counted in any bucket
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Design decisions

- **Method signature follows existing pattern**: Matches `fetch` and `list` methods with `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`.
- **SBOM existence check**: Returns 404 when SBOM is not found, consistent with acceptance criteria and existing SBOM endpoints.
- **Deduplication via HashSet**: Collects unique advisory IDs before counting, satisfying the "counts only unique advisories" acceptance criterion.
- **Error handling with `.context()`**: Every database query uses `.context()` wrapping, matching the project-wide error handling convention from `common/src/error.rs`.
- **Default zero counts**: The `SeveritySummary::default()` initialization ensures all severity levels start at 0, satisfying the "defaults to 0" acceptance criterion.
- **Uses sbom_advisory join table**: As specified in the implementation notes, queries through `entity/src/sbom_advisory.rs` to find linked advisories.
