# File 4: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries the `sbom_advisory` join table, joins to the advisory table, groups advisories by severity level, deduplicates by advisory ID, and returns a `SeveritySummary` struct.

## Detailed Changes

### Change 1: Add import for the new model

At the top of the file, add the import for `SeveritySummary`:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Change 2: Add `severity_summary` method to `AdvisoryService`

Insert a new method in the `AdvisoryService` impl block, following the same pattern as existing `fetch` and `list` methods:

```rust
/// Compute aggregated severity counts for advisories linked to an SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated
/// with the given SBOM ID, deduplicates by advisory ID, and counts the
/// number of advisories at each severity level (critical, high, medium, low).
///
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (Follow the same existence-check pattern used by other service methods)
    
    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(self.db.connection(tx))
        .await
        .context("querying sbom_advisory for severity summary")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisories
        .iter()
        .map(|sa| sa.advisory_id.clone())
        .collect();

    // Fetch the AdvisorySummary for each unique advisory to get severity
    let mut summary = SeveritySummary::default();
    for advisory_id in &unique_advisory_ids {
        // Use existing fetch/service patterns to get advisory details
        // The AdvisorySummary struct has a `severity` field
        if let Some(advisory) = self.fetch(advisory_id.clone(), tx).await? {
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- do not count
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Implementation Notes

- The exact query implementation depends on the actual ORM models and relationships in `entity/src/sbom_advisory.rs`. The code above illustrates the approach; the actual implementation would be refined after inspecting the entity definitions via Serena.
- The SBOM existence check would follow whatever pattern `fetch` uses (e.g., querying the SBOM entity first and returning `AppError::NotFound` if absent).
- Deduplication is performed using a `HashSet` of advisory IDs before counting, satisfying the acceptance criterion for unique advisory counts.
- The `severity` field value matching (e.g., `"critical"`, `"high"`) would be verified against the actual enum or string values used in the `AdvisorySummary.severity` field.
- An alternative, more efficient implementation could use a single SQL query with `GROUP BY severity, COUNT(DISTINCT advisory_id)` -- this would be preferred for the performance acceptance criterion (under 200ms for 500 advisories). The approach above is illustrative; the final implementation would use the most efficient query possible while following SeaORM conventions.

## Conventions Applied

- **Method signature**: Matches existing `fetch` and `list` methods -- takes `&self, id: Id, tx: &Transactional<'_>`
- **Error handling**: Uses `.context()` wrapping with descriptive messages, matching the `AppError` pattern
- **Documentation**: Method has a comprehensive doc comment explaining behavior
- **Naming**: Method named `severity_summary` following `verb_noun` pattern
- **Return type**: Returns `Result<SeveritySummary, AppError>` matching the service method pattern
