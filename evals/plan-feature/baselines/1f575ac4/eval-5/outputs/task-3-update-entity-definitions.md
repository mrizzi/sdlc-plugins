# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new schema: replace the `status_id` foreign key integer field in the `advisory` entity with a `status` field mapped to a Rust enum, and remove the `advisory_status` entity file entirely. This ensures the ORM layer matches the database schema produced by the migration in Task 2.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; define a `AdvisoryStatusEnum` Rust enum with `#[derive(EnumIter, DeriveActiveEnum)]` that maps to the PostgreSQL `advisory_status_enum` type
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` module declaration and any re-exports of the advisory_status entity

## Files to Create
None — the enum definition should live directly in `entity/src/advisory.rs` alongside the entity.

## Implementation Notes
- Follow the SeaORM `DeriveActiveEnum` pattern to map a Rust enum to a PostgreSQL enum type. The derive macro handles serialization/deserialization between Rust and PostgreSQL enum values.
- The Rust enum should be:
  ```rust
  #[derive(Clone, Debug, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
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
- In the `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- In the `Relation` enum, remove the variant that defines the relation to `advisory_status`.
- In the `Column` enum (if manually defined), replace `StatusId` with `Status`.
- Review `entity/src/sbom_advisory.rs` for any references to `advisory_status` — if the join table references it, those references need updating too.
- Look at existing entity files like `entity/src/sbom.rs` or `entity/src/package.rs` for the established pattern of entity definitions in this project.

## Reuse Candidates
- `entity/src/sbom.rs` — example of an established SeaORM entity pattern in this project; follow the same struct layout, derive macros, and relation definitions
- `entity/src/package.rs` — another entity example showing the column and relation patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with DeriveActiveEnum mapping to PostgreSQL `advisory_status_enum`
- [ ] `advisory::Model` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] The `Relation` to `advisory_status` is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` references are removed from `entity/src/lib.rs`
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` passes — entity definitions compile with the new enum type
- [ ] Verify that the `AdvisoryStatusEnum` enum has exactly four variants matching the PostgreSQL enum values

## Verification Commands
- `cargo check -p entity` — entity crate compiles
- `cargo build -p entity` — entity crate builds without warnings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration: advisory_status enum column and drop lookup table
