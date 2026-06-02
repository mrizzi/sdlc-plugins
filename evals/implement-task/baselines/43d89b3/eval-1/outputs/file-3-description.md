# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Current State (expected)
The file contains `AdvisoryService` with methods: `fetch`, `list`, `search`. Each method follows the pattern:
```rust
pub async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<AdvisoryDetails, AppError> {
    // query logic
    // .context("error message") wrapping
}
```

## Changes
Add a new method `severity_summary` to the `impl AdvisoryService` block:

```rust
/// Aggregates advisory severity counts for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts occurrences per
/// severity level (Critical, High, Medium, Low).
///
/// Returns a `SeveritySummary` with counts per severity level and a total.
/// Returns 404 if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404 if not found
    //    (use the same SBOM existence check pattern as other endpoints)

    // 2. Query sbom_advisory join table for distinct advisory IDs linked to this SBOM
    //    Use entity::sbom_advisory to build the query

    // 3. For each linked advisory, fetch its AdvisorySummary to get the severity field

    // 4. Count by severity level into a SeveritySummary struct
    let mut summary = SeveritySummary::default();
    // For each advisory:
    //   match severity {
    //     "Critical" => summary.critical += 1,
    //     "High" => summary.high += 1,
    //     "Medium" => summary.medium += 1,
    //     "Low" => summary.low += 1,
    //     _ => {} // Unknown severity levels are ignored
    //   }
    //   summary.total += 1;

    Ok(summary)
}
```

## Design Decisions
- Method signature matches the established pattern: `&self`, entity ID, transactional context, returns `Result<T, AppError>`.
- SBOM existence is verified first to return a proper 404, consistent with existing SBOM endpoints.
- Advisory deduplication happens at the query level using `DISTINCT` on advisory ID, satisfying the "counts only unique advisories" acceptance criterion.
- The `SeveritySummary::default()` ensures all counts start at 0, satisfying the "defaults to 0" criterion.
- Error wrapping uses `.context()` matching the sibling methods.

## Conventions Applied
- Service method naming: `verb_noun` pattern is slightly adjusted here -- `severity_summary` is a noun describing the returned data, consistent with the domain language.
- Method signature: matches `fetch` and `list` siblings (`&self, id: Id, tx: &Transactional<'_>`).
- Error handling: `Result<T, AppError>` with `.context()` wrapping.
- Documentation: `///` doc comment with description of behavior, parameters, and return/error semantics.

## Imports to Add
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```
