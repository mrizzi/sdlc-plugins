# File 1: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify (existing file)
**Purpose**: Add `severity_summary` method to AdvisoryService

## Pre-Implementation Inspection

Before modifying, would use Serena to inspect:
- `mcp__serena_backend__get_symbols_overview` on this file to see all existing methods
- `mcp__serena_backend__find_symbol` on `AdvisoryService::fetch` with `include_body=true` to understand the method signature pattern
- `mcp__serena_backend__find_symbol` on `AdvisoryService::list` with `include_body=true` to see how list queries work
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to understand all callers

## Changes

Add a new `severity_summary` method to the `AdvisoryService` impl block:

```rust
/// Returns an aggregated severity summary for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts advisories by severity
/// level (Critical, High, Medium, Low). Returns a `SeveritySummary` with counts
/// per severity level and a total count.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (follow the pattern from fetch() for entity existence check)

    // Query sbom_advisory join table for all advisories linked to this SBOM
    // Join with advisory table to get AdvisorySummary data including severity field

    // Deduplicate by advisory ID (using .distinct() or collecting into HashSet)

    // Count advisories per severity level
    // Initialize all counts to 0 (Critical, High, Medium, Low)
    // Iterate through unique advisories, incrementing the appropriate counter

    // Compute total as sum of all severity counts

    // Return SeveritySummary struct
    Ok(SeveritySummary {
        critical: critical_count,
        high: high_count,
        medium: medium_count,
        low: low_count,
        total,
    })
}
```

## Key Patterns Followed

- Method signature follows existing `fetch`/`list` pattern: `&self`, `Id` parameter, `&Transactional<'_>` context
- Returns `Result<SeveritySummary, AppError>` matching the error handling convention
- Uses `.context()` for error wrapping per `common/src/error.rs` pattern
- SBOM existence check returns 404 for non-existent IDs (matching existing SBOM endpoint behavior)
- Single query with join to avoid N+1 (performance requirement: under 200ms for 500 advisories)
- Deduplication by advisory ID per acceptance criteria

## Required Imports

Would need to add import for `SeveritySummary` from the model module:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also imports for the `sbom_advisory` entity:
```rust
use entity::sbom_advisory;
```
