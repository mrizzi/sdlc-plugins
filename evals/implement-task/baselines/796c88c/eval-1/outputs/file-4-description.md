# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates advisories by ID, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

### Inspect before modifying

- Use `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to see exact method signature, parameter types, transaction handling, and error pattern
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` to see alternative query pattern (especially pagination/filtering)
- Use `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` to understand the join table entity structure (columns, relationships)
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to see the `severity` field type and possible values
- Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure the new method does not conflict with existing callers

### New method to add

Add a `severity_summary` method to the `impl AdvisoryService` block:

```rust
/// Compute aggregated severity counts for all advisories linked to an SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the given SBOM ID, deduplicates by advisory ID, and counts each severity
/// level. Returns a `SeveritySummary` with counts defaulting to 0 for levels
/// with no matching advisories.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query advisories linked to this SBOM via the join table
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx)
        .await
        .context("querying sbom_advisory join table")?;

    // Deduplicate by advisory ID
    let unique_advisory_ids: HashSet<_> = advisories
        .iter()
        .map(|a| a.advisory_id)
        .collect();

    // Fetch advisory details to get severity
    let mut summary = SeveritySummary::default();
    for advisory_id in &unique_advisory_ids {
        let advisory = advisory::Entity::find_by_id(*advisory_id)
            .one(tx)
            .await
            .context("fetching advisory")?;
        
        if let Some(adv) = advisory {
            match adv.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown severity levels are not counted
            }
        }
    }
    summary.total = unique_advisory_ids.len() as u64;

    Ok(summary)
}
```

### Notes

- The exact severity field type and possible values must be confirmed by inspecting `AdvisorySummary.severity` — the match arms may need adjustment based on whether severity is an enum, a string, or an option
- The deduplication approach uses `HashSet` to ensure unique advisory IDs per acceptance criteria
- `total` counts all unique advisories regardless of severity level
- If the existing service methods use a different query pattern (e.g., SeaORM `select` with joins rather than separate queries), adapt to match that pattern
- If SBOM does not exist, the method returns a default (all zeros) — the 404 handling for non-existent SBOMs should happen at the endpoint level, consistent with sibling endpoints. Inspect how `get.rs` handles non-existent resources to confirm.
- Error wrapping uses `.context()` per discovered convention
- The method should also handle the case where the SBOM ID does not exist — inspect sibling service methods to see if they return `Option<T>` or `Result<T>` for not-found cases, and match that pattern
- Doc comment on the method per code quality requirements
