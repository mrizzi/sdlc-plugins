# File 1: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct.

## Pre-Change Analysis

Before modifying, read this file to understand:
- The `AdvisoryService` struct definition and its fields (database connection pool, etc.)
- The signatures and implementations of existing methods (`fetch`, `list`, `search`) to replicate the pattern
- How `Transactional<'_>` is used for database access
- Import statements needed for SeaORM queries and error types

## Detailed Changes

### New Import Statements

Add imports for the new model and the join table entity:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

### New Method: `severity_summary`

Add to the `impl AdvisoryService` block:

```rust
/// Returns aggregated severity counts for advisories linked to a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table for all advisories linked to this SBOM
    // 2. Deduplicate by advisory ID (use a HashSet or DISTINCT in the query)
    // 3. For each unique advisory, fetch its severity from the AdvisorySummary model
    // 4. Aggregate counts by severity level
    // 5. Return SeveritySummary with counts and total
    
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query advisories for SBOM")?;

    // Deduplicate by advisory_id
    let unique_advisory_ids: HashSet<_> = advisories
        .iter()
        .map(|a| a.advisory_id)
        .collect();

    let mut summary = SeveritySummary::default();

    for advisory_id in unique_advisory_ids {
        let advisory = self.fetch(advisory_id.into(), tx)
            .await
            .context("Failed to fetch advisory details")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity — skip
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Error Handling

- Uses `.context()` wrapping on all fallible operations, matching the pattern in `common/src/error.rs`
- Returns `Result<SeveritySummary, AppError>` consistent with all other service methods
- The caller (endpoint handler) will translate `AppError` into the appropriate HTTP status code
