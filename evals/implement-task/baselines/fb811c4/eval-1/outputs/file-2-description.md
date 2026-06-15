# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add a `severity_summary` method to the existing `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

### Add imports at the top of the file

Add the following imports (alongside existing imports):

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

### Add `severity_summary` method to `AdvisoryService` impl block

Add the following method after the existing `fetch` and `list` methods, following the same pattern:

```rust
/// Aggregates advisory severity counts for the given SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for each severity level and a total.
///
/// Returns 404 (via `AppError`) if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // Use the sbom service or a direct entity lookup to confirm existence,
    // matching the pattern used in existing SBOM endpoints for 404 handling.

    // Query sbom_advisory join table for advisories linked to this SBOM
    let linked_advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx)
        .await
        .context("Failed to fetch advisories for SBOM")?;

    // Deduplicate by advisory ID (Acceptance Criterion 3)
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in &linked_advisories {
        if !seen.insert(link.advisory_id) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory summary to get the severity field
        // Use the existing AdvisorySummary struct which has a `severity` field
        match &advisory_severity {
            "Critical" | "critical" => summary.critical += 1,
            "High" | "high" => summary.high += 1,
            "Medium" | "medium" => summary.medium += 1,
            "Low" | "low" => summary.low += 1,
            _ => {} // Unknown severity levels are not counted
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Conventions Applied
- **Method signature**: follows the same pattern as `fetch` and `list` -- takes `&self, sbom_id: Id, tx: &Transactional<'_>` and returns `Result<T, AppError>`
- **Error handling**: uses `.context()` wrapping matching the pattern in `common/src/error.rs`
- **Naming**: method name follows the `verb_noun` pattern established by sibling methods
- **Deduplication**: uses `HashSet` to track seen advisory IDs per Acceptance Criterion 3
- **Default values**: `SeveritySummary::default()` ensures all counts start at 0 per Acceptance Criterion 4
- **SBOM existence check**: returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints (Acceptance Criterion 2)

## Notes
- The exact implementation details for fetching severity from linked advisories would depend on the actual schema of `sbom_advisory` and `AdvisorySummary` structs, which would be confirmed during Step 4 code inspection via Serena
- The SBOM existence check pattern would be determined by inspecting how `get.rs` in the SBOM endpoints module handles non-existent IDs
- Performance: for SBOMs with up to 500 advisories, this should execute well under 200ms (Acceptance Criterion 5) -- could be further optimized with a SQL GROUP BY query instead of in-memory aggregation if needed
