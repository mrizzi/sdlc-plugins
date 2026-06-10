# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

**Purpose**: Add a `severity_summary` method to `AdvisoryService` that queries the database for advisory severity counts linked to a given SBOM.

## Detailed Changes

Add a new method to the `AdvisoryService` impl block, following the same pattern as the existing `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all advisories linked to the specified SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the given SBOM, deduplicates by advisory ID, and counts occurrences per severity
/// level (Critical, High, Medium, Low). Returns a `SeveritySummary` with per-level
/// counts and a total.
///
/// Returns an error (mapped to 404) if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // Following the pattern from fetch() which checks existence first
    let _sbom = self
        .sbom_service
        .fetch(sbom_id, tx)
        .await
        .context("fetching SBOM for severity summary")?
        .ok_or_else(|| AppError::not_found(format!("SBOM with id {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    // Deduplicate by advisory ID to count each advisory only once
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("querying advisories for severity summary")?;

    // Count unique advisories per severity level
    let mut seen_ids = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_advisory, advisory) in &advisories {
        if let Some(advisory) = advisory {
            if seen_ids.insert(advisory.id.clone()) {
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or null severity -- not counted in any category
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Conventions Followed

- **Method signature**: `&self, sbom_id: Id, tx: &Transactional<'_>` -- matches the pattern of existing `fetch` and `list` methods in AdvisoryService.
- **Return type**: `Result<SeveritySummary, AppError>` -- consistent with other service methods.
- **Error handling**: `.context("descriptive message")` wrapping throughout, matching `common/src/error.rs` pattern.
- **404 handling**: checks SBOM existence first and returns appropriate error, consistent with existing SBOM endpoints.
- **Deduplication**: uses `HashSet` to track seen advisory IDs, ensuring unique advisory counts per the acceptance criteria.
- **Default zeros**: `SeveritySummary::default()` initializes all counts to 0, satisfying the acceptance criterion for SBOMs with no advisories.
- **Documentation**: doc comment on the method explaining what it does, how it works, and error behavior.
- **Naming**: follows `verb_noun` pattern -- `severity_summary` (consistent with `fetch`, `list`, `search`).

## Serena Usage

Would use:
1. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand the exact method pattern
2. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` to understand query patterns
3. `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` to understand join table columns
4. `mcp__serena_backend__insert_after_symbol` to add the new method after the last existing method in the impl block

## Notes

- The exact query approach (SeaORM API calls, column names, relationship definitions) would be confirmed by inspecting the actual entity definitions and existing query patterns via Serena.
- The severity field access pattern (`advisory.severity`) would be confirmed by inspecting `AdvisorySummary` in `advisory/model/summary.rs`.
- If the severity field uses an enum type rather than a string, the match arms would be adjusted accordingly.
