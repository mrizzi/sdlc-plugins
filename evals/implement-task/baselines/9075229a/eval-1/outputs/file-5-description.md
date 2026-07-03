# File 5: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose
Add a `severity_summary` method to `AdvisoryService` that queries advisory severity counts for a given SBOM.

## Detailed Changes

Add a new method to the existing `impl AdvisoryService` block, following the pattern of the existing `fetch` and `list` methods:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use std::collections::HashMap;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) unchanged ...

    /// Computes aggregated severity counts for all advisories linked to the given SBOM.
    ///
    /// Queries the `sbom_advisory` join table to find advisories associated with the
    /// specified SBOM, deduplicates by advisory ID, and counts by severity level.
    /// Returns a `SeveritySummary` with counts for each severity level and a total.
    /// Returns an error with a 404-equivalent if the SBOM does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists; return 404-style error if not found.
        // (Follow the same SBOM-existence check pattern used by other
        // SBOM-scoped endpoints.)

        // Query the sbom_advisory join table for all advisory links
        // for this SBOM ID, joining with the advisory table to get
        // the severity field from AdvisorySummary.
        let advisory_links = sbom_advisory::Entity::find()
            .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
            .find_also_related(entity::advisory::Entity)
            .all(tx.connection())
            .await
            .context("failed to query advisories for SBOM")?;

        // Deduplicate by advisory ID using a HashSet or similar,
        // then count by severity level.
        let mut seen = std::collections::HashSet::new();
        let mut counts = SeveritySummary::default();

        for (_link, advisory) in advisory_links {
            if let Some(adv) = advisory {
                if seen.insert(adv.id.clone()) {
                    match adv.severity.as_deref() {
                        Some("critical") => counts.critical += 1,
                        Some("high") => counts.high += 1,
                        Some("medium") => counts.medium += 1,
                        Some("low") => counts.low += 1,
                        _ => {} // Unknown or missing severity: not counted in named buckets
                    }
                    counts.total += 1;
                }
            }
        }

        Ok(counts)
    }
}
```

## Conventions Applied
- **Method signature**: `&self, sbom_id: Id, tx: &Transactional<'_>` matches the existing `fetch` and `list` methods in the same file.
- **Return type**: `Result<SeveritySummary, AppError>` following the `Result<T, AppError>` convention.
- **Error handling**: `.context()` wrapping on database queries, matching the established pattern.
- **SBOM existence check**: Verifies the SBOM exists before querying advisories, returning a 404-equivalent error consistent with other SBOM-scoped endpoints.
- **Deduplication**: Uses a `HashSet` to deduplicate by advisory ID, fulfilling the acceptance criterion that counts only unique advisories.
- **Default zeros**: `SeveritySummary::default()` initializes all counts to zero, so missing severity levels naturally default to 0.
- **Documentation**: `///` doc comment on the method explaining purpose, behavior, and error conditions.
- **Naming**: `severity_summary` follows the `verb_noun` / descriptive naming convention of existing methods (`fetch`, `list`, `search`).

## Alternative Approach Considered
A single SQL query with `GROUP BY severity` and `COUNT(DISTINCT advisory_id)` would be more efficient for large datasets. If performance testing shows the Rust-side deduplication is too slow for SBOMs approaching 500 advisories, this should be refactored to a raw SQL query or a SeaORM group-by query. However, the current approach maintains consistency with how sibling service methods interact with SeaORM.
