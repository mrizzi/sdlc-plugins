# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries the database for advisories linked to a given SBOM, deduplicates them, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

### 1. Add import for the new model

At the top of the file, add an import for `SeveritySummary`:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### 2. Add the severity_summary method to AdvisoryService impl block

Following the pattern of existing `fetch` and `list` methods (which take `&self, id: Id, tx: &Transactional<'_>`), add:

```rust
/// Compute aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not found)
    // Use the same SBOM existence check pattern as other SBOM-related endpoints

    // Query sbom_advisory join table for all advisories linked to this SBOM
    // Use entity::sbom_advisory to perform the join

    // Load AdvisorySummary for each linked advisory to access the severity field
    // Deduplicate by advisory ID (use a HashSet or .distinct() in the query)

    // Count by severity level
    let mut summary = SeveritySummary::default();
    // For each unique advisory:
    //   match severity {
    //       "Critical" => summary.critical += 1,
    //       "High" => summary.high += 1,
    //       "Medium" => summary.medium += 1,
    //       "Low" => summary.low += 1,
    //       _ => {} // Unknown severities are not counted
    //   }
    // summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Conventions Applied

- **Method signature**: follows existing `fetch` and `list` pattern -- `&self`, entity ID, `&Transactional<'_>`
- **Return type**: `Result<SeveritySummary, AppError>` matching all other service methods
- **Error handling**: uses `.context()` wrapping for errors, matching `common/src/error.rs` pattern
- **Documentation**: `///` doc comment explaining what the method does, its query strategy, and return value
- **Deduplication**: explicit by advisory ID to satisfy acceptance criterion "Counts only unique advisories"
- **Default zeros**: `SeveritySummary::default()` ensures all counts start at 0

## Inspection Required

Before modifying, would:
1. `mcp__serena_backend__find_symbol` on `AdvisoryService::fetch` with `include_body=true` to see exact method signature and body pattern
2. `mcp__serena_backend__find_symbol` on `AdvisoryService::list` with `include_body=true` to see the list/query pattern
3. `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` to understand join table structure
4. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to verify no callers would break
5. Check how SBOM existence is validated in sibling endpoints (e.g., `SbomService::fetch`)

## Sibling Parity

- Matches `fetch` and `list` methods in the same file for signature style, error handling, and transaction usage
- Uses the same `sbom_advisory` join table referenced in Implementation Notes
