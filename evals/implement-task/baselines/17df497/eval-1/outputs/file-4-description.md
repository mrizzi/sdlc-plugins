# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action:** MODIFY

## Purpose

Add the `severity_summary` method to the existing `AdvisoryService` struct. This method queries the database for advisories linked to a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

### New Method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, alongside the existing `fetch`, `list`, and `search` methods:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

/// Computes aggregated severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisory-SBOM links, fetches
/// the `AdvisorySummary` for each linked advisory, deduplicates by advisory ID,
/// and counts by severity level. Returns a `SeveritySummary` with all counts
/// defaulting to zero when no advisories exist at a given level.
///
/// Returns an error (mapped to 404) if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // This follows the pattern used by existing SBOM endpoints
    let _sbom = self.sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("SBOM not found")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    let linked_advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM-advisory links")?;

    // Deduplicate by advisory ID
    let mut seen_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in &linked_advisories {
        if !seen_ids.insert(link.advisory_id.clone()) {
            continue; // Skip duplicate
        }

        // Fetch the AdvisorySummary to access the severity field
        if let Some(advisory) = self
            .fetch(link.advisory_id.clone(), tx)
            .await
            .context("Failed to fetch advisory")?
        {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown severity levels are not counted
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Alternative: SQL-Level Aggregation (Preferred for Performance)

For the acceptance criterion of "response time under 200ms for SBOMs with up to 500 advisories," a single SQL query with JOIN and GROUP BY would be more performant than N+1 fetches:

```rust
/// Computes aggregated severity counts for all unique advisories linked to the given SBOM.
///
/// Uses a single SQL query with JOIN and GROUP BY for O(1) database round trips,
/// ensuring response time under 200ms even for SBOMs with hundreds of advisories.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists first (404 if not)
    // ... (same SBOM existence check as above)

    // Single query: JOIN sbom_advisory with advisory, GROUP BY severity
    // SELECT severity, COUNT(DISTINCT advisory_id) as count
    // FROM sbom_advisory sa
    // JOIN advisory a ON sa.advisory_id = a.id
    // WHERE sa.sbom_id = $1
    // GROUP BY severity
    let counts = /* SeaORM query using select_column, join, group_by, and count */;

    let mut summary = SeveritySummary::default();
    for (severity, count) in counts {
        match severity.as_str() {
            "Critical" | "critical" => summary.critical = count as u64,
            "High" | "high" => summary.high = count as u64,
            "Medium" | "medium" => summary.medium = count as u64,
            "Low" | "low" => summary.low = count as u64,
            _ => {}
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

The SQL-level approach is preferred because it avoids N+1 queries and achieves the performance requirement. The actual implementation would use SeaORM's query builder to construct this JOIN + GROUP BY query.

### Placement

The method is added inside the existing `impl AdvisoryService` block, after the existing `list` or `search` method.

### New Imports Required

At the top of the file, add:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet; // only if using the in-memory dedup approach
```

### Conventions Applied

- **Method signature**: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>` matches the pattern of `fetch` and `list` methods
- **Error handling**: `.context()` wrapping on database operations, consistent with existing methods
- **Entity access**: uses `entity::sbom_advisory` for the join table query, following SeaORM patterns in the codebase
- **Doc comment**: explains what the method does, its query strategy, and its error behavior
