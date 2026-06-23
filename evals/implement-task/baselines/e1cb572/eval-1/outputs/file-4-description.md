# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action:** MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, joins with advisory data to get severity levels, deduplicates by advisory ID, and returns aggregated counts per severity level.

## Detailed Changes

Add the following method to the `impl AdvisoryService` block, following the existing `fetch` and `list` method signatures:

```rust
/// Computes aggregated severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the SBOM,
/// deduplicates by advisory ID, groups by severity level, and returns counts per level.
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // This follows the pattern used by other SBOM-dependent endpoints
    let _sbom = self
        .sbom_service
        .fetch(sbom_id, tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::NotFound("SBOM not found".into()))?;

    // Query the sbom_advisory join table for advisories linked to this SBOM
    // Use DISTINCT on advisory_id to deduplicate (acceptance criterion 3)
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Build severity counts from unique advisories
    let mut seen_ids = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen_ids.insert(adv.id) {
                match adv.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown severity levels are not counted
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Conventions Applied

- **Method signature:** Follows the same pattern as existing `fetch` and `list` methods: `&self`, entity-specific ID parameter, `tx: &Transactional<'_>`
- **Error handling:** Uses `.context()` wrapping with descriptive messages, matching sibling methods
- **SBOM existence check:** Returns 404 for non-existent SBOM, consistent with existing SBOM endpoints (acceptance criterion 2)
- **Deduplication:** Uses `HashSet` to track seen advisory IDs, ensuring unique counts (acceptance criterion 3)
- **Default zeros:** `SeveritySummary::default()` initializes all counts to 0 (acceptance criterion 4)
- **Documentation:** Method has a doc comment explaining its purpose, query strategy, and return behavior

## Notes

- The exact entity relationships, column names, and severity field access would be confirmed by inspecting `entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`, and `AdvisorySummary.severity` with Serena during Step 4
- The SBOM existence check pattern would be confirmed by inspecting how other endpoints that take an SBOM ID handle the 404 case
- The severity matching logic might use an enum rather than string comparison depending on how the `severity` field is defined in the entity -- would be verified during code inspection
- For performance (acceptance criterion 5: under 200ms for 500 advisories), a single query with GROUP BY would be more efficient than fetching all records and counting in Rust. The actual implementation might use a raw SQL query or SeaORM aggregation if sibling code demonstrates that pattern
