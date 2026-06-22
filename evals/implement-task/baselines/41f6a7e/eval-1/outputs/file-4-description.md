# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries advisories linked to an SBOM and aggregates counts by severity level.

## Detailed Changes

Add a new method `severity_summary` to the existing `AdvisoryService` impl block, following the pattern of existing `fetch` and `list` methods.

### Method to add

```rust
/// Compute aggregated severity counts for all unique advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts advisories at each severity level.
/// Returns a `SeveritySummary` with Critical, High, Medium, Low counts and a total.
///
/// Returns `AppError` with 404 semantics if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not found)
    // This follows the pattern used by existing SBOM endpoints
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Deduplicate by advisory ID using a HashSet
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch each unique advisory to get its severity
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        if let Some(advisory) = self
            .fetch(advisory_id.clone(), tx)
            .await
            .context("Failed to fetch advisory")?
        {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or None severity -- not counted in named buckets but still counted in total
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

### Required imports to add at the top of the file

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Conventions followed

- **Method signature**: Follows existing `fetch` and `list` patterns -- takes `&self`, entity ID, and `&Transactional<'_>`
- **Error handling**: Uses `.context()` wrapping and `AppError` for all fallible operations
- **404 pattern**: Checks SBOM existence first, returns 404 if not found -- consistent with existing SBOM endpoints
- **Naming**: `severity_summary` follows the `verb_noun` naming pattern (treating "severity_summary" as the noun being computed)
- **Documentation**: Full `///` doc comment on the method explaining purpose, behavior, and error semantics

## Notes

- The exact implementation details (field names on entities, query builder syntax) would be confirmed by inspecting the actual code via Serena before writing
- The deduplication approach uses `HashSet` to satisfy the acceptance criterion "Counts only unique advisories (deduplicates by advisory ID)"
- A more performant approach might use a single SQL query with `GROUP BY` and `COUNT`, but the N+1 approach shown here is clearer. If sibling code shows a query-builder pattern for aggregation, that would be preferred. For SBOMs with up to 500 advisories (per acceptance criteria), either approach meets the 200ms requirement.
- The actual severity field type and values would be confirmed from `AdvisorySummary.severity` in `model/summary.rs`
