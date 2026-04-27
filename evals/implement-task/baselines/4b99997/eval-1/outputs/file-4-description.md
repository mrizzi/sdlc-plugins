# File 4: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Action: MODIFY

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that aggregates advisory severity counts for a given SBOM ID.

## Detailed Changes

### New Method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts occurrences per
/// severity level. Returns a `SeveritySummary` with counts for each level and
/// a total. Returns an error (mapped to 404) if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (follow the pattern used by existing fetch methods to check existence)

    // Query sbom_advisory join table for all advisories linked to this SBOM
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query advisories for SBOM")?;

    // Load AdvisorySummary for each unique advisory to access the severity field
    // Deduplicate by advisory ID using a HashSet
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for sa in &advisories {
        if !seen_ids.insert(sa.advisory_id) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory summary to get its severity
        let advisory = AdvisorySummary::from_entity(/* ... */)
            .await
            .context("Failed to load advisory summary")?;

        match advisory.severity.as_deref() {
            Some("critical") => summary.critical += 1,
            Some("high") => summary.high += 1,
            Some("medium") => summary.medium += 1,
            Some("low") => summary.low += 1,
            _ => {} // Unknown or missing severity -- do not count
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### New Imports

Add to the imports section of the file:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

## Conventions Applied

- **Method signature**: Follows the same pattern as `fetch` and `list` -- `async fn method_name(&self, param: Type, tx: &Transactional<'_>) -> Result<T, AppError>`
- **Error wrapping**: Every fallible operation uses `.context()` for descriptive error messages
- **Naming**: `severity_summary` follows the `verb_noun` / `noun_descriptor` pattern used by sibling methods
- **Deduplication**: Uses `HashSet` on advisory IDs to ensure each advisory is counted only once, satisfying the acceptance criterion
- **Default values**: `SeveritySummary::default()` initializes all counts to 0, satisfying the criterion that missing severity levels default to 0
- **SBOM existence check**: Returns 404 for non-existent SBOMs, consistent with existing SBOM endpoints
- **Documentation**: Doc comment on the method describing purpose, query strategy, deduplication, and error behavior
