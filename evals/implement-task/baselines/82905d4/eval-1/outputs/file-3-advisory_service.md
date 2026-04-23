# File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Change

Add the following method to the `impl AdvisoryService` block, following the pattern of existing `fetch` and `list` methods:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;

impl AdvisoryService {
    // ... existing methods (fetch, list, etc.) ...

    /// Aggregate advisory severity counts for a given SBOM.
    ///
    /// Returns a `SeveritySummary` with counts per severity level and a total.
    /// Returns 404 if the SBOM does not exist.
    /// Deduplicates advisories by advisory ID.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // 1. Verify the SBOM exists — return 404 if not found.
        //    Follow the pattern used by existing SBOM-oriented endpoints.
        //    (The exact verification code depends on what's available in the
        //     service layer — likely an SbomService::fetch or a direct entity query.)

        // 2. Query sbom_advisory join table for all advisory IDs linked to this SBOM.
        let db = self.db.connection(tx);
        let sbom_advisories = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
            .all(&db)
            .await
            .context("Error querying sbom_advisory join table")?;

        // 3. Deduplicate by advisory ID.
        let mut seen = HashSet::new();
        let mut summary = SeveritySummary::default();

        for sa in &sbom_advisories {
            if !seen.insert(sa.advisory_id) {
                continue; // Skip duplicate advisory links
            }

            // 4. For each unique advisory, load its summary to get the severity.
            //    Follow the pattern of how AdvisorySummary is constructed elsewhere.
            let advisory = self
                .fetch(sa.advisory_id.into(), tx)
                .await
                .context("Error fetching advisory for severity aggregation")?;

            if let Some(advisory) = advisory {
                // Extract severity from the advisory summary.
                // The exact field access depends on the AdvisorySummary structure
                // discovered during pre-implementation inspection.
                if let Some(ref severity) = advisory.severity {
                    summary.increment(severity);
                } else {
                    summary.total += 1; // Count advisories with no severity
                }
            }
        }

        Ok(summary)
    }
}
```

## Design Decisions

1. **SBOM existence check**: The method must return 404 for non-existent SBOMs. The exact mechanism depends on pre-implementation inspection — it may use `SbomService::fetch` or a direct entity query. If the SBOM is not found, return `AppError::NotFound` (or equivalent).

2. **Deduplication via `HashSet`**: The acceptance criteria require deduplication by advisory ID. A `HashSet<i32>` (or whatever the advisory ID type is) tracks seen IDs in memory. This is efficient for up to 500 advisories (per the performance requirement).

3. **Fallback to database-level deduplication**: If performance inspection reveals the `fetch` call per advisory is too expensive, an alternative approach would use a single SQL query with `SELECT DISTINCT advisory_id, severity FROM sbom_advisory JOIN advisory ...`. This would be more efficient but requires understanding the exact schema. Both approaches should be considered during implementation.

4. **Error wrapping with `.context()`**: Follows the `common/src/error.rs` pattern used throughout the codebase.

5. **Method signature**: Matches existing service methods — `&self`, typed ID parameter, `&Transactional<'_>` for transaction support.

## Performance Consideration

For SBOMs with up to 500 advisories, the current approach of iterating and fetching is acceptable. If the `fetch` method performs complex queries (multiple joins, etc.), the method should be refactored to use a single aggregation query:

```sql
SELECT severity, COUNT(DISTINCT advisory_id) as count
FROM sbom_advisory
JOIN advisory_summary ON advisory_summary.advisory_id = sbom_advisory.advisory_id
WHERE sbom_id = $1
GROUP BY severity
```

This would be implemented as a SeaORM raw query or a custom `Select` with grouping. The decision between the two approaches will be made after inspecting the actual query complexity of `self.fetch()`.
