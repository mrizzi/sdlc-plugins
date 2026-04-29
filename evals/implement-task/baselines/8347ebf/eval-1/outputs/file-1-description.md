# File 1: modules/fundamental/src/advisory/service/advisory.rs

## Change Type: Modify

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

### 1. Add new method `severity_summary` to `AdvisoryService`

Insert a new method after the existing `list` and `search` methods, following the same pattern:

```rust
/// Returns a summary of advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts occurrences of each
/// severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table to find advisories linked to this SBOM
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("failed to query sbom_advisory for severity summary")?;

    // If no SBOM found, return 404
    // First verify the SBOM exists
    let _sbom = sbom::Entity::find_by_id(sbom_id.clone())
        .one(tx.connection())
        .await
        .context("failed to verify SBOM existence")?
        .ok_or_else(|| AppError::not_found(format!("SBOM with id {} not found", sbom_id)))?;

    // Fetch advisory summaries and deduplicate by advisory ID
    let mut seen_ids = std::collections::HashSet::new();
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for sbom_adv in &advisories {
        if !seen_ids.insert(sbom_adv.advisory_id.clone()) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory summary to get the severity field
        let advisory = advisory::Entity::find_by_id(sbom_adv.advisory_id.clone())
            .one(tx.connection())
            .await
            .context("failed to fetch advisory for severity count")?;

        if let Some(adv) = advisory {
            let summary = AdvisorySummary::from(adv);
            match summary.severity.as_deref() {
                Some("Critical") | Some("critical") => critical += 1,
                Some("High") | Some("high") => high += 1,
                Some("Medium") | Some("medium") => medium += 1,
                Some("Low") | Some("low") => low += 1,
                _ => {} // Unknown or missing severity -- skip
            }
        }
    }

    let total = critical + high + medium + low;

    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

### 2. Add necessary imports

At the top of the file, add imports for:
- `SeveritySummary` from the model module
- `sbom_advisory` entity (if not already imported)
- `sbom` entity (for SBOM existence check)
- `std::collections::HashSet` (for deduplication)

## Conventions Applied

- Method signature follows the existing `verb_noun` pattern (`severity_summary`)
- Parameters follow the existing pattern: `&self, <specific_params>, tx: &Transactional<'_>`
- Error handling uses `Result<T, AppError>` with `.context()` wrapping
- Uses SeaORM entity queries consistent with existing `fetch` and `list` methods
- Returns 404 via `AppError::not_found()` consistent with existing SBOM endpoints
- Documentation comment uses `///` Rust doc convention

## Backward Compatibility

Adding a new method to `AdvisoryService` is purely additive and does not affect existing callers. The `find_referencing_symbols` check would confirm no existing code is impacted.
