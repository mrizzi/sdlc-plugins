# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and returns counts grouped by severity level.

## Current state (inspected via Serena)

The `AdvisoryService` struct has existing methods:
- `fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<Option<AdvisoryDetails>, Error>`
- `list(&self, ..., tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, Error>`
- `search(&self, ..., tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, Error>`

All methods follow the same pattern: take `&self`, accept a transactional context, return `Result<T, Error>`.

## Changes

Add the following method to the `impl AdvisoryService` block:

```rust
/// Returns an aggregated severity summary for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, and counts occurrences of each severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, Error> {
    // Fetch the SBOM to verify it exists; return 404-equivalent error if not found
    // (following the pattern in SbomService::fetch)
    let sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| Error::NotFound(format!("SBOM with id {} not found", sbom_id)))
        .context("fetching SBOM for severity summary")?;

    // Query sbom_advisory join table for all advisories linked to this SBOM
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("querying sbom_advisory links")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch advisory summaries for unique IDs and count by severity
    let mut summary = SeveritySummary::default();
    for advisory_id in unique_advisory_ids {
        if let Some(advisory) = self.fetch(advisory_id, tx).await? {
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- do not count
            }
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Additional imports needed at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use std::collections::HashSet;
```

## Conventions applied

- Method signature follows `verb_noun` pattern: `severity_summary`
- Takes `&self, id: Id, tx: &Transactional<'_>` matching existing service methods
- Returns `Result<T, Error>` with `.context()` wrapping for error chains
- Uses `ok_or_else` for not-found errors, matching `fetch` pattern
- Documentation comment on the public method explaining purpose and behavior
