## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new advisory status enum schema. Replace the `status_id` foreign key relation in the advisory entity with a direct `status` enum column, and remove the `advisory_status` entity entirely. This aligns the ORM layer with the migration from Task 2.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation::AdvisoryStatus` variant and its `RelationDef`; add `AdvisoryStatusEnum` enum with SeaORM `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` — Remove `mod advisory_status` and its re-export from the entity registry

## Implementation Notes
Follow the existing entity patterns in `entity/src/advisory.rs` for column definitions and relation setup.

For the enum column, use SeaORM's `DeriveActiveEnum` derive macro to define `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`. The enum maps to the PostgreSQL `advisory_status_enum` type created by the migration. Example pattern:

```rust
#[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
pub enum AdvisoryStatusEnum {
    #[sea_orm(string_value = "New")]
    New,
    #[sea_orm(string_value = "Analyzing")]
    Analyzing,
    #[sea_orm(string_value = "Fixed")]
    Fixed,
    #[sea_orm(string_value = "Rejected")]
    Rejected,
}
```

Remove the `advisory_status` entity module registration in `entity/src/lib.rs` — this entity file will no longer exist as the lookup table is dropped.

## Reuse Candidates
- `entity/src/advisory.rs::Model` — Existing advisory entity model to modify in-place
- `entity/src/advisory.rs::Relation` — Existing relation enum to remove the `AdvisoryStatus` variant from

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` and variants New, Analyzing, Fixed, Rejected
- [ ] `advisory::Model` has `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] `advisory::Relation` no longer includes `AdvisoryStatus` variant
- [ ] `entity/src/lib.rs` no longer references `advisory_status` module
- [ ] `entity/src/advisory_status.rs` is deleted (or confirmed non-existent if the entity was defined inline)
- [ ] Entity crate compiles successfully (`cargo check -p entity`)

## Test Requirements
- [ ] Entity crate compiles without errors
- [ ] `AdvisoryStatusEnum` correctly derives `DeriveActiveEnum` with all four variants
- [ ] No remaining references to `advisory_status` entity or `status_id` column in the entity crate

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
