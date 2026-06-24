# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table and aggregates advisory severity counts for a given SBOM.

## Detailed Changes

Add a new method to the `impl AdvisoryService` block, following the existing pattern of `fetch` and `list`:

```rust
/// Computes aggregated advisory severity counts for the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts advisories by severity
/// level (Critical, High, Medium, Low). Returns a [`SeveritySummary`] with all
/// counts defaulting to zero when no advisories exist at a given level.
///
/// Returns `AppError` with 404 semantics when the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not)
    // This follows the pattern in existing SBOM endpoints
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM {sbom_id} not found")))?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    // Deduplicate by advisory ID using DISTINCT
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx)
        .await
        .context("failed to query advisories for SBOM")?;

    // Count unique advisories by severity level
    let mut summary = SeveritySummary::default();
    let mut seen_ids = std::collections::HashSet::new();

    for (sbom_adv, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            // Deduplicate by advisory ID
            if !seen_ids.insert(advisory.id.clone()) {
                continue;
            }

            // Fetch the AdvisorySummary to access the severity field
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- still counted in total
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

## Convention Conformance

- **Method signature**: Follows the `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>` pattern used by `fetch` and `list`.
- **Error handling**: Uses `.context()` wrapping for database errors and `AppError::not_found()` for 404s, matching the pattern in `common/src/error.rs`.
- **Entity access**: Uses SeaORM's `Entity::find()` with `.filter()` and `.find_also_related()`, consistent with existing query patterns.
- **Naming**: Method name `severity_summary` follows the `verb_noun` convention seen in existing methods (`fetch`, `list`, `search`).
- **Documentation**: Full `///` doc comment on the method explaining behavior, parameters, and error semantics.
- **Deduplication**: Uses a `HashSet` to deduplicate by advisory ID per acceptance criteria.

## Notes

The exact implementation details (column names, entity relationships, severity field access) would be verified during Step 4 by inspecting `entity/src/sbom_advisory.rs`, `entity/src/advisory.rs`, and the `AdvisorySummary` struct's `severity` field in `modules/fundamental/src/advisory/model/summary.rs`. The code above represents the intended pattern; actual field names and types would be adjusted based on code inspection.
