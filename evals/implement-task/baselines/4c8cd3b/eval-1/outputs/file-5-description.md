# File 5: modules/fundamental/src/advisory/service/advisory.rs

**Action:** MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM, deduplicates them, counts by severity level, and returns a `SeveritySummary`.

## Detailed Changes

Add the following method to the existing `AdvisoryService` impl block, after the existing `fetch` and `list` methods:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) remain unchanged ...

    /// Aggregates advisory severity counts for a given SBOM.
    ///
    /// Queries the `sbom_advisory` join table to find all advisories linked to the
    /// specified SBOM, deduplicates by advisory ID, and counts per severity level.
    /// Returns a `SeveritySummary` with counts for Critical, High, Medium, Low, and total.
    /// Returns an error with 404 semantics if the SBOM does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: &Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Verify the SBOM exists; return 404 if not found
        // (reuse existing SBOM existence check pattern from SbomService)
        let _sbom = self
            .sbom_service
            .fetch(sbom_id, tx)
            .await
            .context("SBOM not found")?;

        // Query sbom_advisory join table for all advisories linked to this SBOM
        let advisory_links = entity::sbom_advisory::Entity::find()
            .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
            .all(tx.connection())
            .await
            .context("Failed to query SBOM advisory links")?;

        // Collect unique advisory IDs to deduplicate
        let unique_advisory_ids: HashSet<_> = advisory_links
            .iter()
            .map(|link| link.advisory_id.clone())
            .collect();

        // Fetch each unique advisory's summary to get the severity field
        let mut summary = SeveritySummary::default();

        for advisory_id in &unique_advisory_ids {
            let advisory = self
                .fetch(advisory_id, tx)
                .await
                .context("Failed to fetch advisory details")?;

            // Use the severity field from AdvisorySummary to classify
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or None severity -- not counted in any bucket
            }
        }

        summary.total = summary.critical + summary.high + summary.medium + summary.low;

        Ok(summary)
    }
}
```

## Key Design Decisions

1. **SBOM existence check first:** The method verifies the SBOM exists before querying advisories, returning a 404-equivalent error if not found. This matches the acceptance criterion "Returns 404 when SBOM ID does not exist."

2. **Deduplication via HashSet:** Advisory IDs are collected into a `HashSet` before counting, ensuring each advisory is counted at most once even if the join table contains duplicate links. This satisfies the "Counts only unique advisories" criterion.

3. **Default to zero:** `SeveritySummary::default()` initializes all counts to 0, so severity levels without any advisories naturally produce zero counts.

4. **Case-insensitive severity matching:** The match handles both title-case and lowercase severity strings for robustness.

## Conventions Applied

- **Method signature:** Follows the same pattern as `fetch` and `list` -- takes `&self`, entity ID reference, and transaction reference.
- **Error handling:** Uses `.context()` wrapping on every fallible operation, consistent with all other service methods.
- **Naming:** Method name `severity_summary` follows the `verb_noun` / descriptive pattern used by sibling methods.
- **Documentation:** Method has a comprehensive doc comment explaining behavior, parameters, and error semantics.
