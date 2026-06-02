## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema. Modify the `advisory` entity to replace the `status_id` foreign key column with a `status` column of type `advisory_status_enum`. Remove the `advisory_status` entity entirely since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; remove the relation to `advisory_status`; add the `AdvisoryStatusEnum` enum definition (or import it) with SeaORM `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export

## Files to Create
None — the enum type is defined inline in the advisory entity or as a submodule

## Implementation Notes
Follow the existing SeaORM entity pattern in `entity/src/sbom.rs` for entity struct definition and column enumeration. For the enum mapping, use SeaORM's `DeriveActiveEnum` macro to map the `advisory_status_enum` PostgreSQL type to a Rust enum:

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

Remove the relation definition from `advisory.rs` that references the `advisory_status` table (the `Relation::HasOne` or `Relation::BelongsTo` pointing to `AdvisoryStatus`).

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct definition pattern, column enumeration, and relation definitions
- `entity/src/package.rs` — reference for entity pattern with related tables

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `advisory` entity `Model` struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] Relation to `advisory_status` is removed from advisory entity
- [ ] `entity/src/lib.rs` no longer declares or exports the `advisory_status` module
- [ ] `entity/src/advisory_status.rs` is deleted (or its contents are no longer referenced)
- [ ] Code compiles with `cargo check -p entity`

## Test Requirements
- [ ] `cargo check -p entity` passes with no errors
- [ ] The `AdvisoryStatusEnum` correctly maps to the PostgreSQL `advisory_status_enum` type

## Verification Commands
- `cargo check -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
