## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema. Modify `entity/src/advisory.rs` to replace the `status_id` integer foreign key column with a `status` column using the `advisory_status_enum` PostgreSQL enum type. Remove the `entity/src/advisory_status.rs` file entirely since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status` table
- `entity/src/lib.rs` — remove `pub mod advisory_status;` module declaration

## Files to Create
None — the enum type mapping will be defined within `entity/src/advisory.rs`

## Implementation Notes
- In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::EnumIter`, `sea_orm::DeriveActiveEnum` to map it to the PostgreSQL `advisory_status_enum` type.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in `advisory.rs` and its corresponding `RelationTrait` implementation.
- Remove any `Related<advisory_status::Entity>` implementation from `advisory.rs`.
- Use `#[sea_orm(enum_name = "advisory_status_enum")]` on the enum and `#[sea_orm(string_value = "New")]` etc. on each variant to match the PostgreSQL enum values exactly.
- The `status` column in the `Model` struct should be typed as `AdvisoryStatusEnum`.
- Reference the existing entity pattern in `entity/src/sbom.rs` for struct layout and derive macros.
- Deleting `entity/src/advisory_status.rs`: this file contains the SeaORM entity for the now-dropped `advisory_status` table. It must be fully removed, not left as dead code.
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing entity code before modifying; follow established patterns.

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct patterns, derive macros, and relation definitions
- `entity/src/package.rs` — reference for entity patterns if sbom.rs does not demonstrate enum column usage

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants mapped to PostgreSQL enum
- [ ] `entity/src/advisory.rs` `Model` struct has `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `entity/src/advisory.rs` no longer has a `Relation` to `advisory_status`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares the `advisory_status` module
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] Run `cargo build -p entity` to verify compilation
- [ ] Run `cargo test -p entity` to verify no test regressions

## Verification Commands
- `cargo build -p entity` — expected: compiles without errors
- `cargo check -p entity` — expected: no warnings about dead code or unused imports

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
