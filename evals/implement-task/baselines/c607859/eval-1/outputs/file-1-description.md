# File 1: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY (add method to existing service)

## Context

This file contains the `AdvisoryService` struct with existing methods `fetch`, `list`, and `search`. The new `severity_summary` method follows the same pattern as these existing methods.

## Sibling Pattern Reference

Existing methods in this file follow a consistent signature pattern:
- Take `&self` as the receiver
- Accept domain-specific ID parameters
- Accept `tx: &Transactional<'_>` for database transaction context
- Return `Result<T, AppError>` with `.context()` error wrapping
- Use SeaORM queries against entities in the `entity/` crate

## Changes

Add a new method `severity_summary` to the `AdvisoryService` impl block:

```rust
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// SBOM, deduplicates by advisory ID, and counts occurrences per severity level.
/// Returns a `SeveritySummary` with counts for critical, high, medium, low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (follow the pattern used in existing fetch methods for 404 handling)
    let sbom_exists = /* query sbom entity by sbom_id */;
    if !sbom_exists {
        return Err(AppError::not_found(format!("SBOM {} not found", sbom_id)))
            .context("looking up SBOM for advisory severity summary");
    }

    // Query sbom_advisory join table to find all advisory IDs linked to this SBOM
    // Use DISTINCT to deduplicate advisory IDs (acceptance criterion: unique advisories only)
    let advisories = SbomAdvisory::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(Advisory)
        .all(tx)
        .await
        .context("querying advisories for SBOM severity summary")?;

    // Deduplicate by advisory ID using a HashSet
    let mut seen_ids = HashSet::new();
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for (sbom_adv, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen_ids.insert(advisory.id) {
                // Build AdvisorySummary to access the severity field
                // (following the pattern from the existing list/fetch methods)
                match advisory.severity.as_deref() {
                    Some("critical") | Some("Critical") => critical += 1,
                    Some("high") | Some("High") => high += 1,
                    Some("medium") | Some("Medium") => medium += 1,
                    Some("low") | Some("Low") => low += 1,
                    _ => {} // Unknown severity levels are not counted
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

## Imports to Add

At the top of the file, add:
```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

## Error Handling

- SBOM not found: returns 404 `AppError` consistent with existing SBOM endpoints
- Database query failure: uses `.context()` wrapping consistent with all sibling methods
- No advisories: returns `SeveritySummary` with all zeros (default values)

## Contract & Sibling Parity

- **Signature parity**: matches `fetch` and `list` method signatures (`&self`, ID param, `tx` param, `Result<T, AppError>` return)
- **Error handling parity**: uses `.context()` wrapping like all other methods in this service
- **Transaction handling parity**: accepts `&Transactional<'_>` like all sibling methods
- **Entity usage parity**: queries through SeaORM entity relations like existing methods
