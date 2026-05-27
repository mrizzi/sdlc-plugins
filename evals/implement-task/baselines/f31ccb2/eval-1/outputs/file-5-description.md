# File 5: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

### Current State (inferred from task description and repository structure)

The `AdvisoryService` struct has existing methods:
- `fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<Option<AdvisorySummary>, AppError>` — fetches a single advisory
- `list(&self, /* params */, tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, AppError>` — lists advisories with pagination

### New Method: `severity_summary`

Add the following method to the `impl AdvisoryService` block:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

/// Aggregates advisory severity counts for a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level and a total.
/// Returns an error with 404 status if the SBOM does not exist.
/// Deduplicates advisories by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists
    //    Use SbomService::fetch or a direct entity query to confirm the SBOM ID is valid.
    //    If not found, return AppError (404 variant).
    let _sbom = /* sbom existence check */
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // 2. Query the sbom_advisory join table for all advisory IDs linked to this SBOM
    //    Uses entity::sbom_advisory::Entity to find related advisory records.
    let sbom_advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query sbom_advisory table")?;

    // 3. Deduplicate by advisory ID
    let unique_advisory_ids: HashSet<_> = sbom_advisories
        .iter()
        .map(|sa| sa.advisory_id)
        .collect();

    // 4. Fetch AdvisorySummary for each unique advisory to get severity
    //    Could batch-fetch or iterate. The severity field on AdvisorySummary
    //    contains the severity level string.
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        if let Some(advisory) = self.fetch(*advisory_id, tx).await? {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or None severity — not counted in any bucket
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

### Implementation Notes

1. **SBOM existence check**: The exact mechanism depends on whether `AdvisoryService` has access to an `SbomService` or can query the SBOM entity directly. Options:
   - If `AdvisoryService` holds a reference to the database connection pool, query `entity::sbom::Entity::find_by_id(sbom_id)` directly
   - If there's a cross-service reference, delegate to `SbomService::fetch()`
   - The specific approach should match whatever pattern existing service methods use for cross-entity queries

2. **Deduplication**: Uses `HashSet<advisory_id>` to ensure each advisory is counted exactly once, even if the `sbom_advisory` join table has multiple entries for the same advisory-SBOM pair.

3. **Severity matching**: The `match` on severity handles both capitalized and lowercase variants for robustness. The exact severity values should be confirmed from the data model, but the task description specifies Critical, High, Medium, Low.

4. **Total counting**: `total` counts all unique advisories regardless of severity level, including those with unknown/null severity. This ensures `total` accurately reflects the number of linked advisories.

5. **Performance consideration**: For SBOMs with up to 500 advisories (per acceptance criteria), this approach of fetching each advisory individually could be slow. An optimized version would use a single SQL query with GROUP BY on severity. The implementation should be verified against the performance requirement and potentially refactored:

   ```sql
   SELECT a.severity, COUNT(DISTINCT sa.advisory_id)
   FROM sbom_advisory sa
   JOIN advisory a ON a.id = sa.advisory_id
   WHERE sa.sbom_id = $1
   GROUP BY a.severity
   ```

   This could be implemented as a raw SeaORM query or via the query builder with `.group_by()`.

6. **Error propagation**: Uses `.context()` wrapping consistent with `common/src/error.rs` patterns.

## Conventions Applied

- Method signature follows `fetch` and `list` patterns: `&self`, domain param, `tx: &Transactional<'_>`
- Returns `Result<T, AppError>` matching all other service methods
- Error handling via `.context()` wrapping
- Uses SeaORM entity queries for database access
- Doc comment on the public method
