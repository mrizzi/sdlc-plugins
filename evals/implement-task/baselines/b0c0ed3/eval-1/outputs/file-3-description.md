# File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM, deduplicates by advisory ID, groups by severity, and returns a `SeveritySummary`.

## Detailed Changes

### New import (add at top of file)

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also ensure these entity imports are present (add if missing):

```rust
use entity::sbom_advisory;
```

### New method on `AdvisoryService` (add inside the `impl AdvisoryService` block)

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (critical, high,
/// medium, low) and a total. Advisories are deduplicated by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // 1. Query the sbom_advisory join table to find all advisory IDs linked to this SBOM.
    let linked_advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("failed to query sbom_advisory for severity summary")?;

    // 2. Collect unique advisory IDs to deduplicate.
    let unique_advisory_ids: HashSet<_> = linked_advisories
        .iter()
        .map(|rel| rel.advisory_id.clone())
        .collect();

    // 3. If no advisories are linked, return default (all zeros).
    if unique_advisory_ids.is_empty() {
        return Ok(SeveritySummary::default());
    }

    // 4. Fetch the AdvisorySummary for each unique advisory to read its severity.
    let mut summary = SeveritySummary::default();
    for advisory_id in &unique_advisory_ids {
        let advisory = self
            .fetch(advisory_id.clone(), tx)
            .await
            .context("failed to fetch advisory for severity aggregation")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("Critical" | "critical") => summary.critical += 1,
                Some("High" | "high") => summary.high += 1,
                Some("Medium" | "medium") => summary.medium += 1,
                Some("Low" | "low") => summary.low += 1,
                _ => {} // Unknown or None severity — not counted in named buckets
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Design Decisions

- **Deduplication**: Uses `HashSet` on advisory ID to satisfy the acceptance criterion of counting only unique advisories.
- **Default zeros**: `SeveritySummary::default()` ensures all counts are 0 when no advisories are linked.
- **Severity matching**: Case-insensitive matching on the first character handles both "Critical" and "critical" forms. The match arms cover all four named severity levels; unknown values are silently ignored (counted in total only if desired, but current spec implies only four levels).
- **Error handling**: Uses `.context()` wrapping consistent with `fetch` and `list` method patterns.
- **Transaction parameter**: Follows the established `tx: &Transactional<'_>` pattern from sibling methods.

## Convention Conformance

- Method signature matches `fetch` and `list` patterns: `&self`, domain ID parameter, transactional reference.
- Error wrapping with `.context()` matches `common/src/error.rs` usage.
- Uses existing `self.fetch()` to leverage already-tested code paths for loading advisory data.
- Import of `HashSet` from `std::collections` if not already imported.
