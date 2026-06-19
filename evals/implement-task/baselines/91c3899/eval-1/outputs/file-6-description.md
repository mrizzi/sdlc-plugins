# File 6: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table to count advisories by severity level for a given SBOM ID, returning a `SeveritySummary` struct.

## Sibling Reference

The existing `AdvisoryService` has `fetch` and `list` methods that follow this pattern:
```rust
impl AdvisoryService {
    pub async fn fetch(
        &self,
        id: Id,
        tx: &Transactional<'_>,
    ) -> Result<Option<AdvisoryDetails>, AppError> {
        // query logic with .context() error wrapping
    }

    pub async fn list(
        &self,
        // pagination/filter params
        tx: &Transactional<'_>,
    ) -> Result<PaginatedResults<AdvisorySummary>, AppError> {
        // query logic
    }
}
```

The new method follows the same signature pattern: `&self`, domain-specific params, `tx`, returns `Result<T, AppError>`.

## Detailed Changes

Add the following method to the `AdvisoryService` `impl` block:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

/// Computes aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates them by advisory ID, and counts each severity level.
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Given: verify the SBOM exists, returning 404 if not found
    // (Follow the pattern used by existing SBOM endpoints for existence checks)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // When: query advisories linked to this SBOM via the sbom_advisory join table
    // Use DISTINCT on advisory ID to deduplicate
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query advisories for SBOM")?;

    // Then: count unique advisories by severity level
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_advisory, advisory) in advisories {
        if let Some(advisory) = advisory {
            // Deduplicate by advisory ID
            if !seen_ids.insert(advisory.id.clone()) {
                continue;
            }

            // Count by severity level
            match advisory.severity.as_deref() {
                Some("Critical") => summary.critical += 1,
                Some("High") => summary.high += 1,
                Some("Medium") => summary.medium += 1,
                Some("Low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- do not count
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

## Design Notes

- **SBOM existence check**: The method first verifies the SBOM exists before querying advisories. If the SBOM is not found, it returns a 404 error via `AppError::not_found()`, consistent with existing SBOM endpoint behavior (acceptance criterion 2).

- **Deduplication**: Uses a `HashSet` to track seen advisory IDs and skip duplicates. This satisfies acceptance criterion 3 (counts only unique advisories). An alternative approach would be using `SELECT DISTINCT` in the SQL query, but the HashSet approach is explicit and testable. If performance is a concern for very large datasets, the query could be refactored to use SQL-level `DISTINCT` and `GROUP BY`.

- **Default to zero**: The `SeveritySummary::default()` initializes all counts to 0, satisfying acceptance criterion 4.

- **Performance**: For the acceptance criterion of under 200ms for up to 500 advisories, this approach queries all linked advisories in a single database call and counts in memory. For larger scale, this could be optimized to use a SQL `GROUP BY` aggregation query, but for 500 records the in-memory approach is efficient.

- **Error handling**: Uses `.context()` wrapping on all fallible operations, matching the project convention.

- **Method signature**: Follows the established pattern of `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`, matching `fetch` and `list` methods.

- **Severity matching**: The match statement handles the four known severity levels (Critical, High, Medium, Low). Unknown or missing severity values are silently skipped -- they are not counted toward any severity level but are also not counted in the total. This is a design decision; if the project prefers to count all advisories regardless of severity, the total increment would move before the match statement. The current approach ensures `total == critical + high + medium + low`, which is cleaner for dashboard display.

- **Import additions**: The `use` statements for `SeveritySummary`, `HashSet`, and any entity imports should be added at the top of the file alongside existing imports.
