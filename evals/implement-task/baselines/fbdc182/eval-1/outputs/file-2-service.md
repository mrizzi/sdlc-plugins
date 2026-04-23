# File 2 — Modify: `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose

Add a `severity_summary` async method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates advisory IDs, and returns a `SeveritySummary` count struct.

## Inspection Step

Read `modules/fundamental/src/advisory/service/advisory.rs` in full (or via `get_symbols_overview` + `find_symbol` with `include_body=true` for `fetch` and `list`) to understand:
- Existing `use` imports (SeaORM prelude, entity paths, `AppError`, `Transactional`)
- How `fetch` resolves a single advisory (for the 404 pattern)
- How `list` queries with joins (for the join table pattern)
- The exact type alias for `Transactional<'_>` (may be `DatabaseTransaction` or a project wrapper)

Also read `entity/src/sbom_advisory.rs` to know the column names on the join table (likely `sbom_id`, `advisory_id`, and a `severity` column — or the severity may come from joining `entity/src/advisory.rs`).

Also read `modules/fundamental/src/advisory/model/severity_summary.rs` (created in File 4) to know the import path.

## New Method to Add

Add after the existing `list` method (or at the end of the `impl AdvisoryService` block), following the same signature pattern as `fetch` and `list`:

```rust
/// Returns a count of unique advisories per severity level for the given SBOM.
///
/// Returns `AppError::not_found` if the SBOM does not exist.
/// Deduplicates advisories that are linked more than once via the join table.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists — return 404 if not found
    // (mirrors the pattern in SbomService::fetch, confirmed by reading that method)
    use entity::sbom::Entity as SbomEntity;
    let sbom_exists = SbomEntity::find_by_id(sbom_id)
        .one(tx.as_ref())
        .await
        .context("failed to look up SBOM")?;
    if sbom_exists.is_none() {
        return Err(AppError::not_found(format!("SBOM with id {sbom_id} not found")));
    }

    // Query the sbom_advisory join table, selecting distinct advisory_id and severity.
    // Severity is sourced from the advisory entity (joined), matching the AdvisorySummary.severity field.
    use entity::advisory::Entity as AdvisoryEntity;
    use entity::sbom_advisory::Entity as SbomAdvisoryEntity;
    use sea_orm::{ColumnTrait, EntityTrait, QueryFilter, QuerySelect};

    // Fetch all distinct (advisory_id, severity) pairs for the given sbom_id.
    // Using a raw select to get both columns efficiently.
    let rows = SbomAdvisoryEntity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .inner_join(AdvisoryEntity)
        .select_only()
        .column(entity::sbom_advisory::Column::AdvisoryId)
        .column(entity::advisory::Column::Severity)
        .distinct()
        .into_tuple::<(Id, Option<String>)>()
        .all(tx.as_ref())
        .await
        .context("failed to query advisory severity summary")?;

    // Aggregate counts by severity level
    let mut summary = SeveritySummary::default();
    for (_advisory_id, severity) in rows {
        match severity.as_deref() {
            Some("Critical") => summary.critical += 1,
            Some("High") => summary.high += 1,
            Some("Medium") => summary.medium += 1,
            Some("Low") => summary.low += 1,
            _ => {} // unknown / None severity — not counted in named levels
        }
        summary.total += 1;
    }

    Ok(summary)
}
```

## Import additions at top of file

Add the following `use` statements alongside the existing imports (only if not already present):

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

(The SeaORM and entity imports are likely already present from `fetch` / `list` — only add what is missing after reading the file.)

## Notes on severity field

The exact column name and string values for severity must be confirmed by reading `entity/src/advisory.rs`. If the column uses an enum type instead of `String`, adjust the match arms to use the enum variants. The `AdvisorySummary` struct in `model/summary.rs` uses a `severity` field — reading that struct confirms the representation in use.

## Convention compliance

- Signature matches `fetch`/`list`: `(&self, id: Id, tx: &Transactional<'_>) -> Result<T, AppError>`
- Error wrapping: `.context("...")` on every `.await?` call
- 404 pattern: checks entity existence first, returns `AppError::not_found(...)` if absent
- `///` doc comment on the new public method
