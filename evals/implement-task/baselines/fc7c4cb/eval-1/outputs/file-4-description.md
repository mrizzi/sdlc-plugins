# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add the `severity_summary` method to the existing `AdvisoryService` struct.

## Pre-Implementation Inspection

Before modifying, inspect this file using:
- `mcp__serena_backend__get_symbols_overview` to see the `AdvisoryService` struct and all its methods
- `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the exact method signature pattern
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to confirm all callers and ensure the new method signature is compatible

## Detailed Changes

### Add method: `severity_summary`

Insert a new method on `AdvisoryService` after the existing `list` or `search` method, using `insert_after_symbol` via Serena:

```rust
/// Computes an aggregated severity summary for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts for critical, high, medium, and low
/// severities, plus a total count.
///
/// Returns `AppError::NotFound` if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::NotFound("SBOM not found".to_string()))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("querying sbom_advisory join table")?;

    // Fetch unique advisory details and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for link in &advisories {
        if !seen.insert(link.advisory_id.clone()) {
            continue; // deduplicate by advisory ID
        }

        if let Some(summary) = self
            .fetch(link.advisory_id.clone(), tx)
            .await?
        {
            match summary.severity.as_deref() {
                Some("critical") => critical += 1,
                Some("high") => high += 1,
                Some("medium") => medium += 1,
                Some("low") => low += 1,
                _ => {} // unknown or missing severity still counted in total
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

### Additional imports needed at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use anyhow::Context as _;
use std::collections::HashSet;
```

(Only add imports that are not already present.)

### Design Decisions

- **Method signature**: Follows the exact pattern of `fetch` and `list` -- takes `&self`, an ID parameter, and `tx: &Transactional<'_>`, returns `Result<T, AppError>`.
- **SBOM existence check**: First verifies the SBOM exists before querying advisories, returning 404 if not found (acceptance criterion).
- **Deduplication**: Uses a `HashSet` to track seen advisory IDs, ensuring duplicate links in `sbom_advisory` are counted only once (acceptance criterion).
- **Severity matching**: Matches on the `severity` field from `AdvisorySummary`, which was identified during code inspection in Step 4.
- **Error handling**: Uses `.context()` for wrapping database errors, matching the project convention.
- **Doc comment**: Comprehensive `///` documentation explaining the method's purpose, behavior, and error cases.

### Convention Conformance

- `Result<T, AppError>` return type with `.context()` wrapping
- Method signature matches existing `fetch` and `list` methods
- `verb_noun` naming: `severity_summary`
