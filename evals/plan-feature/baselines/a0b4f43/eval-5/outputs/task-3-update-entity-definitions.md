## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the enum migration. Modify `entity/src/advisory.rs` to replace the `status_id` integer foreign key column with a `status` column using the `advisory_status_enum` type. Remove the `entity/src/advisory_status.rs` entity file since the lookup table no longer exists. Deregister the `advisory_status` module from `entity/src/lib.rs`.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the `Relation` to `advisory_status`; add a Rust enum `AdvisoryStatusEnum` mapped to the PostgreSQL `advisory_status_enum` type via SeaORM's `DeriveActiveEnum`
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` declaration
- `entity/Cargo.toml` — verify SeaORM enum derive features are enabled (if not already)

## Files to Create
None — all changes are modifications to existing files. The `AdvisoryStatusEnum` Rust enum will be defined inline in `entity/src/advisory.rs`.

## Implementation Notes
- In `entity/src/advisory.rs`, define the Rust enum using SeaORM's derive macros:
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
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in `advisory.rs` and its corresponding `RelationDef` implementation.
- Remove any `Related<advisory_status::Entity>` implementation from `advisory.rs`.
- Delete the file `entity/src/advisory_status.rs` entirely.
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for structure consistency.
- Per `docs/constraints.md` §5.1 (Code Change Rules): changes must be scoped to listed files only.
- Per `docs/constraints.md` §5.2: inspect existing entity code before modifying.
- Per `docs/constraints.md` §2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005.

## Reuse Candidates
- `entity/src/sbom.rs` — existing SeaORM entity demonstrating the project's entity definition pattern
- `entity/src/package.rs` — another entity example for consistent structure

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` has a `status` column of type `AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The `Relation::AdvisoryStatus` variant and related impl are removed from `advisory.rs`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares `pub mod advisory_status`
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] Verify the entity crate compiles: `cargo check -p entity`
- [ ] Verify that no other entity files reference `advisory_status` module

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main