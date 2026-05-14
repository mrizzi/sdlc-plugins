# File 4: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose
Add the `severity_summary` method to `AdvisoryService` that aggregates advisory
severity counts for a given SBOM.

## Sibling Reference
Follows the pattern of existing `fetch` and `list` methods in the same file --
method signature takes `&self`, entity ID, and `tx: &Transactional<'_>`, returns
`Result<T, AppError>`.

## Detailed Changes

### Add import for the new model

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also add any needed imports for the join table entity and deduplication:

```rust
use entity::sbom_advisory;
use std::collections::HashSet;
```

### Add `severity_summary` method to `impl AdvisoryService`

Add the following method inside the existing `impl AdvisoryService` block,
after the existing `fetch`, `list`, and `search` methods:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with per-level counts and total.
///
/// Returns `AppError` with 404 status if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // Use the same SBOM existence check pattern as other endpoints
    let _sbom = self
        .db
        .find_sbom_by_id(sbom_id, tx)
        .await
        .context("looking up SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(advisory::Entity)
        .all(tx.connection())
        .await
        .context("fetching advisories for SBOM")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_link, advisory_opt) in advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id) {
                match advisory.severity.as_deref() {
                    Some("Critical") => summary.critical += 1,
                    Some("High") => summary.high += 1,
                    Some("Medium") => summary.medium += 1,
                    Some("Low") => summary.low += 1,
                    _ => {} // Unknown or missing severity -- skip but still count in total
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Notes
- The method follows the same pattern as `fetch` and `list`: takes `&self`, an ID parameter, and `tx: &Transactional<'_>`.
- SBOM existence is checked first, returning 404 if not found (matching existing SBOM endpoint behavior).
- Uses `HashSet` for deduplication by advisory ID (satisfying: "Counts only unique advisories").
- Uses `SeveritySummary::default()` to initialize all counts to 0 (satisfying: "All severity levels default to 0").
- Severity matching uses the `severity` field from `AdvisorySummary` as referenced in the Implementation Notes.
- Error wrapping uses `.context()` per the convention in `common/src/error.rs`.
- The exact entity/column names, relationship access pattern, and SBOM existence check would be confirmed by reading the actual sibling code via Serena before implementation.
- For performance with up to 500 advisories, a single query with join is sufficient (no N+1 queries). For even better performance, a SQL aggregation query could be used instead of loading all records into memory, but the in-memory approach is simple and performant enough for 500 records.
