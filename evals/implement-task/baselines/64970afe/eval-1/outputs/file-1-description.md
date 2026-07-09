# File 1: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Pre-modification inspection

Before modifying this file, inspect it using:
- `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` to see the full struct and method listing for `AdvisoryService`.
- `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to read the exact method signature and body of the `fetch` method, which the Implementation Notes reference as the pattern to follow.
- `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to read the `list` method as an additional reference.

Also inspect the join table entity:
- `mcp__serena_backend__get_symbols_overview("entity/src/sbom_advisory.rs")` to understand the SBOM-Advisory join table structure.

And the severity field on AdvisorySummary:
- `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` in `modules/fundamental/src/advisory/model/summary.rs` to confirm the `severity` field's type and values.

## Changes

Add a new `severity_summary` method to the `impl AdvisoryService` block. The method follows the same pattern as the existing `fetch` and `list` methods.

### New method: `severity_summary`

```rust
/// Returns an aggregated severity summary of all advisories linked to the given SBOM.
///
/// Counts unique advisories by severity level (Critical, High, Medium, Low) and returns
/// the totals. Advisories linked multiple times to the same SBOM are deduplicated by
/// advisory ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = self.sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))
        .context("looking up SBOM for severity summary")?;

    // Query advisories linked to this SBOM via the sbom_advisory join table,
    // deduplicating by advisory ID
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("querying advisories for SBOM")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id.clone()) {
                match adv.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or None severity -- not counted
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

### Import additions

At the top of the file, add:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Conventions followed

- **Method signature**: Matches `fetch` and `list` pattern -- `&self`, entity ID, `tx: &Transactional<'_>`.
- **Return type**: `Result<SeveritySummary, AppError>` -- consistent with all service methods.
- **Error handling**: Uses `.context("description")` wrapping on all fallible operations.
- **Naming**: `severity_summary` follows `verb_noun` / `noun_noun` pattern used by existing methods.
- **Documentation**: Doc comment on the public method explaining what it does and the deduplication behavior.

### Backward compatibility

No existing methods are modified. The new method is purely additive. Checked via `mcp__serena_backend__find_referencing_symbols` that no existing code references a `severity_summary` symbol.
