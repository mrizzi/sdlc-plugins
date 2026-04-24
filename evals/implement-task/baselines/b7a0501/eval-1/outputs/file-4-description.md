# File 4: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Action: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries advisories linked to
a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a
`SeveritySummary` struct.

## Sibling Reference

- Existing methods in this file: `fetch`, `list`, `search`
- These methods follow the pattern: `pub async fn method_name(&self, params..., tx: &Transactional<'_>) -> Result<T, AppError>`
- They use SeaORM queries, `.context()` error wrapping, and return domain model types.

## Detailed Changes

### 1. Add import for the new model

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### 2. Add `severity_summary` method to `AdvisoryService` impl block

Insert a new method in the `impl AdvisoryService` block, following the pattern of `fetch`
and `list`:

```rust
/// Computes aggregated severity counts for advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts occurrences at each
/// severity level (Critical, High, Medium, Low).
///
/// Returns a 404 error if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (Follow the pattern used by existing SBOM-lookup methods)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisory links")?;

    // Deduplicate by advisory ID
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in advisory_links {
        if !seen_ids.insert(link.advisory_id.clone()) {
            continue; // Skip duplicate advisory
        }

        // Fetch the advisory summary to get its severity
        let advisory = self
            .fetch(link.advisory_id, tx)
            .await
            .context("Failed to fetch advisory")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or null severity -- not counted in named levels but still counted in total
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

## Conventions Applied

- **Method signature**: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>` -- matches the `fetch` and `list` method signatures.
- **Error handling**: `.context()` wrapping on all fallible operations, matching sibling methods.
- **404 handling**: Returns `AppError::not_found()` when the SBOM does not exist, consistent
  with existing SBOM endpoint 404 behavior.
- **Deduplication**: Uses `HashSet` to track seen advisory IDs, satisfying the acceptance
  criterion for unique advisory counts.
- **Default zeros**: `SeveritySummary::default()` initializes all counts to 0, satisfying
  the acceptance criterion.
- **Doc comment**: Full `///` doc comment on the method explaining behavior and error cases.

## Notes

- The exact entity column names, ID types, and query builder patterns would be confirmed
  by inspecting `entity/src/sbom_advisory.rs` and the existing `fetch`/`list` methods
  via Serena in a real implementation.
- The SBOM existence check pattern would be verified against how other endpoints handle
  SBOM lookups -- the `SbomService.fetch()` call may need adjustment based on the actual API.
- Performance consideration: For SBOMs with many advisories, a single SQL GROUP BY query
  would be more efficient than individual fetches. In a real implementation, this would be
  optimized to use a database-level aggregation query, but the above illustrates the logic.
  The optimized version would look like:

  ```sql
  SELECT a.severity, COUNT(DISTINCT a.id) as count
  FROM sbom_advisory sa
  JOIN advisory a ON sa.advisory_id = a.id
  WHERE sa.sbom_id = $1
  GROUP BY a.severity
  ```

  This would satisfy the performance requirement of under 200ms for up to 500 advisories.
