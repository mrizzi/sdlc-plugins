# File 1 -- Modify: `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` impl block.

## Pre-Implementation Inspection

Before modifying, inspect this file using Serena (`mcp__serena_backend__get_symbols_overview`)
to understand the existing structure. Specifically:
- Confirm the `AdvisoryService` struct and its impl block exist.
- Confirm the `fetch` and `list` methods exist and understand their signatures.
- Identify the `Transactional` type import and the `Id` type used for parameters.

Also inspect `entity/src/sbom_advisory.rs` using `mcp__serena_backend__find_symbol` to
understand the join table entity structure (columns, relations) for querying advisories
linked to an SBOM.

Inspect `modules/fundamental/src/advisory/model/summary.rs` to confirm the `AdvisorySummary`
struct has a `severity` field and understand its type (likely `Option<String>` or an enum).

## Changes

### Add import for the new model

At the top of the file, add an import for the `SeveritySummary` struct:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Add `severity_summary` method

Insert a new method in the `AdvisoryService` impl block, following the pattern of `fetch`
and `list`. The method:

1. **Signature**: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, anyhow::Error>`
2. **SBOM existence check**: First verify the SBOM exists by querying the sbom table. If not
   found, return an appropriate `AppError::NotFound` or `anyhow::bail!` with context, matching
   the 404 pattern used by sibling methods.
3. **Query advisories**: Use the `sbom_advisory` join table to find all advisories linked to
   the given `sbom_id`. Join to the advisory table to access the `severity` field from
   `AdvisorySummary`.
4. **Deduplicate**: Use `.distinct()` or `GROUP BY advisory_id` to ensure each advisory is
   counted only once, even if linked multiple times via different SBOM-advisory relationships.
5. **Count by severity**: Group results by severity level and count occurrences. Map severity
   values to the four levels: Critical, High, Medium, Low. Any unrecognized severity values
   should be excluded from the named counts but still included in `total`.
6. **Build response**: Construct a `SeveritySummary` with the counts, defaulting each level
   to 0 if no advisories exist at that severity.
7. **Error wrapping**: Wrap all database errors with `.context("fetching advisory severity summary for SBOM")`.

### Example implementation sketch

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Returns counts of unique advisories per severity level (Critical, High,
/// Medium, Low) and a total count. Advisories linked multiple times to the
/// same SBOM are deduplicated by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Verify SBOM exists (return 404 if not)
    // ... query sbom table ...

    // Query unique advisories linked to this SBOM via sbom_advisory join table
    // ... SeaORM query with join and distinct ...

    // Count by severity level
    let mut critical = 0i64;
    let mut high = 0i64;
    let mut medium = 0i64;
    let mut low = 0i64;
    let mut total = 0i64;

    for advisory in advisories {
        total += 1;
        match advisory.severity.as_deref() {
            Some("Critical" | "critical") => critical += 1,
            Some("High" | "high") => high += 1,
            Some("Medium" | "medium") => medium += 1,
            Some("Low" | "low") => low += 1,
            _ => {} // Unknown severity still counted in total
        }
    }

    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

## Conventions Applied

- Method signature follows `verb_noun` pattern (`severity_summary`).
- Takes `&self`, identifier, and `&Transactional<'_>` matching sibling methods.
- Returns `Result<T, anyhow::Error>` with `.context()` wrapping.
- Doc comment on the public method explains behavior, parameters, and deduplication logic.
