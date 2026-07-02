# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries the `sbom_advisory` join table, aggregates advisory severity counts for a given SBOM ID, deduplicates by advisory ID, and returns a `SeveritySummary` struct.

## Pre-implementation Inspection

Before modifying this file, thoroughly inspect the existing code:

1. **Overview**: Use `mcp__serena_backend__get_symbols_overview` on this file to see all existing methods on `AdvisoryService`
2. **Pattern study**: Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand:
   - Method signature pattern (`&self`, parameter types, `Transactional` usage)
   - How SeaORM queries are constructed
   - Error handling pattern (`.context()` wrapping)
   - Return type pattern
3. **Pattern study (list)**: Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method to see how collection queries differ from single-entity queries
4. **Backward compatibility**: Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure the struct is not instantiated in a way that would break with the new method (it should not, since we are adding a method, not changing the struct definition)
5. **Join table inspection**: Use `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` to understand the join table entity columns (sbom_id, advisory_id)
6. **Severity field**: Use `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to understand the severity field type and possible values

## Planned Changes

Add the following method to the `impl AdvisoryService` block:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries advisories linked to the specified SBOM via the `sbom_advisory`
/// join table, deduplicates by advisory ID, and returns counts per severity
/// level (critical, high, medium, low) along with the total unique count.
pub async fn severity_summary(
    &self,
    sbom_id: &Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = SbomService::fetch(sbom_id, tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id.clone()) {
                match advisory.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {} // Unknown or null severity not counted in named buckets
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Design Decisions

- **SBOM existence check**: Returns 404 when SBOM ID does not exist, satisfying acceptance criterion. Follows the pattern used by other endpoints that validate parent entity existence.
- **Deduplication via HashSet**: Uses a `HashSet<advisory_id>` to ensure each advisory is counted only once, even if the join table contains duplicate links. Satisfies acceptance criterion "Counts only unique advisories."
- **Default struct**: `SeveritySummary::default()` starts all counts at 0, satisfying "All severity levels default to 0."
- **Match on severity string**: The severity field from `AdvisorySummary` is matched against known severity levels. Unknown values are counted in `total` but not in any named bucket.
- **Error handling**: `.context()` wrapping on all fallible operations, matching the established convention.
- **Method placement**: Added at the end of the `impl AdvisoryService` block, after existing methods.

## Notes

- The exact query construction (SeaORM entity paths, column names, relationship traversal) will be confirmed by inspecting the actual entity definitions before implementation
- If the project uses a different SBOM existence check pattern (e.g., a dedicated `exists` query), that pattern will be used instead
- The severity field type (string, enum, etc.) will be confirmed from the `AdvisorySummary` struct before writing the match arms
- Performance: single query with join avoids N+1; in-memory aggregation is efficient for up to 500 advisories (per acceptance criteria)

## Conventions Applied

- Method signature: `&self, id, tx` pattern matching `fetch` and `list`
- Return type: `Result<T, AppError>`
- Error handling: `.context()` wrapping
- Doc comment: `///` with description of purpose and behavior
