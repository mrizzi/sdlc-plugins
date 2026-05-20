# File 4: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add the `get_severity_summary` method to `AdvisoryService` that queries the database for advisory severity counts linked to a given SBOM, deduplicates by advisory ID, and returns a `SeveritySummary`.

## Conventions Applied

- Method follows the same pattern as existing `fetch` and `list` methods on `AdvisoryService`
- Takes `&self`, `sbom_id: Id`, and `tx: &Transactional<'_>` parameters
- Returns `Result<SeveritySummary, anyhow::Error>`
- Uses SeaORM query builder for database access
- Uses `.context()` for error wrapping
- First validates that the SBOM exists (returning 404 if not)

## Change Description

### New imports (add at top of file if not already present)

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use std::collections::HashSet;
```

### New method (add inside `impl AdvisoryService { ... }` block)

```rust
/// Compute aggregated severity counts for all advisories linked to the given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level and a total.
/// Deduplicates advisories by advisory ID to avoid double-counting.
pub async fn get_severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // First, verify the SBOM exists (return 404 if not)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {sbom_id} not found")))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(self.db.connection(tx))
        .await
        .context("Failed to query advisories for SBOM")?;

    // Deduplicate by advisory ID and count by severity
    let mut summary = SeveritySummary::default();
    let mut seen_ids = HashSet::new();

    for (_link, advisory_opt) in advisory_links {
        if let Some(advisory) = advisory_opt {
            if seen_ids.insert(advisory.id) {
                // Use the advisory's severity field to classify
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or missing severity -- counted in total but not in any bucket
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Design Decisions

1. **SBOM existence check first**: Before querying advisories, we verify the SBOM exists using the existing `sbom_service.fetch()` method. This ensures a clean 404 response for non-existent SBOMs, consistent with other SBOM endpoints.

2. **Application-level deduplication**: Uses a `HashSet<Id>` to track seen advisory IDs. An alternative would be to use `SELECT DISTINCT` at the SQL level with `GROUP BY severity`, which would be more efficient for very large datasets. The application-level approach is shown here for clarity, but the SQL approach would be preferred if performance profiling indicates it is needed.

3. **Case-insensitive severity matching**: The match arms handle both capitalized ("Critical") and lowercase ("critical") variants to be robust against data inconsistencies. The exact casing should be verified against the actual data in the `advisory` table.

4. **Unknown/missing severity**: Advisories with unknown or missing severity values are still counted in `total` but not attributed to any severity bucket. This ensures `total` always equals the true count of unique advisories.

5. **No pagination needed**: This method returns a single aggregated result, not a list, so `PaginatedResults` is not used.

## Alternative: SQL-Level Aggregation

For better performance at scale (meeting the "under 200ms for 500 advisories" requirement), the query could be rewritten as a single SQL aggregation:

```sql
SELECT
    COUNT(DISTINCT CASE WHEN a.severity = 'Critical' THEN a.id END) AS critical,
    COUNT(DISTINCT CASE WHEN a.severity = 'High' THEN a.id END) AS high,
    COUNT(DISTINCT CASE WHEN a.severity = 'Medium' THEN a.id END) AS medium,
    COUNT(DISTINCT CASE WHEN a.severity = 'Low' THEN a.id END) AS low,
    COUNT(DISTINCT a.id) AS total
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
```

This can be expressed in SeaORM using raw SQL or custom expressions. The choice between application-level and SQL-level aggregation depends on the actual data volumes and performance requirements.
