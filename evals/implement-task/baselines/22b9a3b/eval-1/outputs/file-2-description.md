# File 2: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct. This method queries the `sbom_advisory` join table to find all advisories linked to a given SBOM, deduplicates them by advisory ID, fetches each advisory's severity, and returns a `SeveritySummary` with counts per severity level.

## Sibling Reference

The existing `fetch` and `list` methods in this file establish the conventions:
- Method signature: `&self`, domain-specific ID, `tx: &Transactional<'_>`
- Error handling: Return `Result<T, AppError>` with `.context()` wrapping
- Database access: SeaORM queries through entity modules

## Detailed Changes

### Import Additions

Add to the existing imports at the top of the file:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use std::collections::HashSet;
```

### New Method

Add the following method to the `impl AdvisoryService` block, after the existing `list` and/or `search` methods:

```rust
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
///
/// Deduplicates advisories by ID to ensure each advisory is counted only once,
/// even if linked multiple times through the join table.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // First verify the SBOM exists, returning 404 if not found
    let sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))
        .context("Looking up SBOM for advisory summary")?;

    // Query all advisory links for this SBOM via the join table
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("Querying SBOM-advisory links")?;

    // Deduplicate by advisory ID
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in &advisory_links {
        if !seen_ids.insert(link.advisory_id.clone()) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory summary to access its severity field
        if let Some(advisory) = self
            .fetch(link.advisory_id.clone(), tx)
            .await?
        {
            match advisory.severity.as_deref() {
                Some("critical") | Some("Critical") => summary.critical += 1,
                Some("high") | Some("High") => summary.high += 1,
                Some("medium") | Some("Medium") => summary.medium += 1,
                Some("low") | Some("Low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- not counted in any bucket
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Design Notes

- **SBOM existence check**: The method first verifies the SBOM exists so it can return a proper 404 rather than silently returning all zeros for a non-existent SBOM. This matches the acceptance criterion: "Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints."
- **Deduplication**: Uses a `HashSet` to track advisory IDs already counted. This satisfies the acceptance criterion: "Counts only unique advisories (deduplicates by advisory ID)."
- **Case-insensitive severity matching**: Matches both lowercase and title-case severity strings to be robust against data inconsistencies.
- **Total calculation**: Computed as the sum of all four severity buckets, ensuring consistency.
- **Performance note**: For SBOMs with up to 500 advisories this approach is acceptable. For larger scale, a SQL `GROUP BY` query on severity would be more efficient, but the current approach maintains consistency with the existing service method patterns that fetch individual records.
- An alternative, more performant implementation could use a single SQL query with `GROUP BY` on the severity column joined through `sbom_advisory`, avoiding N+1 queries. This optimization could be noted as a follow-up if performance testing reveals issues.
