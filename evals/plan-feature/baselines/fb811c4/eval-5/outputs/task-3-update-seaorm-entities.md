## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the enum migration. The `advisory` entity must replace the `status_id` foreign key field with a `status` field using the `advisory_status_enum` PostgreSQL enum type. The entity file for the `advisory_status` lookup table must be removed since the table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add a SeaORM `DeriveActiveEnum` enum definition for `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- `entity/src/lib.rs` — Remove the `advisory_status` module re-export; add the `AdvisoryStatusEnum` type to public exports if needed

## Files to Create
(none — the advisory_status entity file is removed, not created)

## Implementation Notes
Follow the existing entity pattern in `entity/src/advisory.rs` for the `Model` derive and column definitions. SeaORM supports PostgreSQL enums via the `DeriveActiveEnum` macro — define an enum like:

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

Remove the `advisory_status` entity file and its reference in `entity/src/lib.rs`. Update `entity/Cargo.toml` if any dependencies were specific to the lookup table entity.

Also check `entity/src/sbom_advisory.rs` for any references to `advisory_status` that need updating.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with DeriveActiveEnum macro
- [ ] `entity/src/advisory.rs` Model struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] Relation to `advisory_status` is removed from advisory entity
- [ ] `advisory_status` entity file is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] Project compiles with `cargo check` (entity crate)

## Test Requirements
- [ ] Verify entity compiles correctly with `cargo check -p entity`
- [ ] Verify the enum serializes/deserializes correctly by writing a unit test for AdvisoryStatusEnum round-trip

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 2 — Database migration for advisory status enum

[sdlc-workflow] Description digest: sha256-md:64e9a166e6fcdc2bd0aa8efb617ba3cea249bf7c417d24990b2742e80747ab4b
