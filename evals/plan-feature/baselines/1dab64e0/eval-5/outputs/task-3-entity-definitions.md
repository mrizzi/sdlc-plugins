## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory schema after the enum migration. Replace the `status_id` foreign key field in the `advisory` entity with a `status` field of enum type `AdvisoryStatusEnum`. Remove the `advisory_status` entity file since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key column with `status: AdvisoryStatusEnum` enum column; remove the `Relation` to `advisory_status`; define the `AdvisoryStatusEnum` as a SeaORM `DeriveActiveEnum` with values `New`, `Analyzing`, `Fixed`, `Rejected`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export
- `entity/src/advisory_status.rs` — remove this file entirely (the advisory_status lookup table entity is no longer needed)
- `entity/Cargo.toml` — no changes expected, but verify no advisory_status-specific dependencies exist

## Implementation Notes
Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` derive macro. The enum should map to the PostgreSQL `advisory_status_enum` type created by the migration in Task 2.

Example pattern for SeaORM enum definition:
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

Remove the `RelationDef` for `AdvisoryStatus` from the `advisory` entity's `Relation` enum and remove any `Related<advisory_status::Entity>` implementation.

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for domain modules; entity changes must align with module boundaries.
Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — example SeaORM entity definition without FK-based lookup table, demonstrating the standard entity pattern with direct column types

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` mapping to `advisory_status_enum` PostgreSQL type
- [ ] The `advisory` entity's `Column` enum replaces `StatusId` with `Status` of enum type
- [ ] The `advisory` entity's `Relation` enum no longer includes a relation to `advisory_status`
- [ ] `entity/src/advisory_status.rs` is removed
- [ ] `entity/src/lib.rs` no longer declares or exports the `advisory_status` module
- [ ] The entity crate compiles successfully with `cargo build -p entity`

## Test Requirements
- [ ] `cargo build -p entity` compiles without errors after entity changes
- [ ] Any existing entity unit tests continue to pass
- [ ] The `AdvisoryStatusEnum` can be used in SeaORM queries (column filtering, insertion)

## Verification Commands
- `cargo build -p entity` — entity crate compiles without errors
- `cargo test -p entity` — entity tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum conversion
