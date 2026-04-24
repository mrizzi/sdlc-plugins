# File 6: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, retrieves all advisories linked to a given SBOM, deduplicates by advisory ID, counts each severity level, and returns a `SeveritySummary` struct.

## Conventions Applied

- **Method signature**: Follows the `fetch`/`list` pattern -- `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- **Error handling**: Uses `.context()` wrapping for descriptive error messages, returns `Result<T, AppError>`
- **Transaction parameter**: Accepts `&Transactional<'_>` as the last parameter, consistent with all other `AdvisoryService` methods
- **Naming**: `severity_summary` follows the `verb_noun` or `noun_noun` pattern seen in the service (alongside `fetch`, `list`, `search`)

## Current State (expected)

`AdvisoryService` has methods like:

```rust
impl AdvisoryService {
    pub async fn fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<AdvisoryDetails, AppError> {
        // ...
    }

    pub async fn list(&self, /* params */, tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, AppError> {
        // ...
    }

    pub async fn search(&self, /* params */, tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, AppError> {
        // ...
    }
}
```

## Change Description

Add the `severity_summary` method to the `impl AdvisoryService` block:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

impl AdvisoryService {
    // ... existing methods ...

    /// Computes aggregated severity counts for all advisories linked to the specified SBOM.
    ///
    /// Queries the `sbom_advisory` join table to find all advisories associated with the
    /// given SBOM ID, deduplicates by advisory ID, and counts the number of advisories
    /// at each severity level (Critical, High, Medium, Low).
    ///
    /// Returns a 404 error if the SBOM does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists; return 404 if not found
        // (Use existing SBOM lookup pattern from SbomService or equivalent)
        let _sbom = self
            .verify_sbom_exists(sbom_id, tx)
            .await
            .context("verifying SBOM exists for severity summary")?;

        // Query the sbom_advisory join table for all advisories linked to this SBOM
        let advisory_links = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
            .all(tx.connection())
            .await
            .context("querying advisory links for SBOM")?;

        // Deduplicate by advisory ID
        let mut seen_ids = HashSet::new();
        let unique_advisory_ids: Vec<_> = advisory_links
            .into_iter()
            .filter(|link| seen_ids.insert(link.advisory_id.clone()))
            .map(|link| link.advisory_id)
            .collect();

        // Fetch the severity for each unique advisory
        let mut summary = SeveritySummary::default();

        for advisory_id in &unique_advisory_ids {
            let advisory = self
                .fetch(*advisory_id, tx)
                .await
                .context("fetching advisory for severity count")?;

            // The AdvisorySummary struct has a `severity` field
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- not counted in any bucket
            }
        }

        summary.total = unique_advisory_ids.len() as u64;

        Ok(summary)
    }
}
```

## Design Decisions

1. **SBOM existence check first**: Returns 404 early if the SBOM doesn't exist, satisfying the acceptance criterion "Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints". The exact mechanism (`verify_sbom_exists` or querying the SBOM entity directly) would be determined from the actual codebase.

2. **HashSet-based deduplication**: Uses a `HashSet` to track seen advisory IDs, ensuring each advisory is counted only once even if it appears multiple times in the join table. This satisfies "Counts only unique advisories (deduplicates by advisory ID)".

3. **Case-insensitive severity matching**: Matches both "Critical" and "critical" to handle potential data inconsistencies. The actual casing would be verified from existing data during implementation.

4. **Total counts all unique advisories**: `total` is computed from the unique advisory count, not from the sum of severity buckets. This ensures advisories with unknown severity are included in the total but not in any severity bucket. Whether this is correct would be verified with the user if the actual codebase reveals unknown severity values.

5. **Individual fetch per advisory**: The initial implementation fetches each advisory individually. If performance profiling shows this doesn't meet the "Response time under 200ms for SBOMs with up to 500 advisories" requirement, this would be optimized to a batch query with a `GROUP BY severity` clause at the database level, avoiding the N+1 query pattern.

## Performance Note

The implementation above uses an N+1 query pattern (one query for join table, then N queries for individual advisories). For the 200ms performance requirement with up to 500 advisories, a more optimized approach would be:

```rust
// Optimized: single query with JOIN and GROUP BY
let counts = entity::sbom_advisory::Entity::find()
    .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
    .inner_join(entity::advisory::Entity)
    .select_only()
    .column(entity::advisory::Column::Severity)
    .column_as(entity::advisory::Column::Id.count(), "count")
    .group_by(entity::advisory::Column::Severity)
    .into_tuple::<(String, i64)>()
    .all(tx.connection())
    .await
    .context("aggregating advisory severities for SBOM")?;
```

This optimized query performs the aggregation at the database level, reducing the operation to a single query regardless of advisory count. The exact SeaORM API and column names would be verified during implementation.

## Scope

Only the `severity_summary` method is added. No existing methods are modified. All imports are added at the top of the file without disturbing existing imports.
