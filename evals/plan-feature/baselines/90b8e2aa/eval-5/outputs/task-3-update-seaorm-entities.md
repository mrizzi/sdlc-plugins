# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status schema. The `advisory` entity must replace its `status_id` integer FK field with a `status` field of the new `AdvisoryStatusEnum` type. The `advisory_status` entity module must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status` and update the `Model` struct
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and any re-exports referencing it

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` (or a shared location) using SeaORM's `DeriveActiveEnum` derive macro:
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
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum and its corresponding `RelationDef` implementation.
- Remove the file `entity/src/advisory_status.rs` entirely — it defines the SeaORM entity for the now-dropped `advisory_status` lookup table.
- Follow the existing entity patterns in `entity/src/sbom.rs` for struct layout and derive macros.
- Per CONVENTIONS.md §Framework: use SeaORM's `DeriveActiveEnum` for enum column mapping.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's database framework scope.

## Reuse Candidates
- `entity/src/sbom.rs` — sibling entity demonstrating the project's SeaORM entity struct pattern, derive macros, and relation definitions
- `entity/src/advisory.rs` — current advisory entity to understand the existing `status_id` field, relations, and model structure before modifying

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The `Model` struct in `advisory.rs` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] The `Relation::AdvisoryStatus` variant is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` passes with no errors or warnings related to the entity changes
- [ ] Verify that no other entity files reference `advisory_status` or `status_id`

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion
