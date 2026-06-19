# File 1: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify (add method)

## Current State

This file contains `AdvisoryService` with existing methods: `fetch`, `list`, `search`. Each method follows the pattern:
- Takes `&self`, entity-specific parameters, and `tx: &Transactional<'_>`
- Returns `Result<T, AppError>`
- Uses SeaORM query builders to access the database
- Wraps errors with `.context("descriptive message")`

## Changes

Add a new `severity_summary` method to `AdvisoryService`. Insert it after the existing methods (e.g., after `list` or `search`), following the established pattern.

### New method: `severity_summary`

```rust
/// Returns aggregated severity counts for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts each severity
/// level. Returns a `SeveritySummary` with counts for Critical, High, Medium,
/// Low, and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // First verify the SBOM exists -- return 404 if not found
    // (follow the pattern used by existing fetch methods)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    // Use .distinct() or collect into a HashSet to deduplicate by advisory ID
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Deduplicate by advisory ID
    let mut seen = std::collections::HashSet::new();
    let mut critical = 0u32;
    let mut high = 0u32;
    let mut medium = 0u32;
    let mut low = 0u32;

    for (_sbom_advisory, advisory) in &advisories {
        if let Some(advisory) = advisory {
            if seen.insert(advisory.id.clone()) {
                // Use the severity field from AdvisorySummary pattern
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => critical += 1,
                    Some("High") | Some("high") => high += 1,
                    Some("Medium") | Some("medium") => medium += 1,
                    Some("Low") | Some("low") => low += 1,
                    _ => {} // Unknown or None severity -- do not count
                }
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

### Required imports to add at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Rationale

- Method signature follows the same pattern as `fetch` and `list`: `&self`, entity ID, transaction context
- SBOM existence check ensures 404 is returned for non-existent SBOMs, matching acceptance criteria
- Deduplication via `HashSet` ensures unique advisory counting per acceptance criteria
- `.context()` wrapping on all fallible operations matches the error handling convention
- Severity matching is case-insensitive to handle potential data inconsistencies
- All counters default to 0 (Rust's default for u32), satisfying the "default to 0" acceptance criterion
- Single query with join avoids N+1 problem, supporting the performance requirement
