# File 2: `migration/src/m0002_drop_advisory_status/mod.rs` (Create)

## Purpose

New migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Pre-inspection

Before creating this file, inspect the sibling migration `migration/src/m0001_initial/mod.rs` to understand:
- Import statements used (SeaORM migration prelude, entity references)
- Struct definition pattern for the `Migration` struct
- `MigrationTrait` implementation structure (`up` and `down` method signatures)
- How the `SchemaManager` API is used for DDL operations
- How entity table/column enums are referenced (e.g., `Advisory::Table`, `Advisory::Status`)

Also verify in `entity/src/advisory.rs`:
- That the `Advisory` enum has `Table` and `Status` variants available for use in the migration
- That the entity model struct does NOT have a `status` field (confirming it was already removed)

## File Content

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer referenced by any service or
/// entity code.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .drop_column(Advisory::Status)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Advisory::Table)
                    .add_column(ColumnDef::new(Advisory::Status).string().null())
                    .to_owned(),
            )
            .await
    }
}

/// Enum referencing the advisory table and its columns for use in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`up` method:** Uses `TableAlterStatement` with `drop_column(Advisory::Status)` as specified in the Implementation Notes. This is the standard SeaORM pattern for removing a column.

2. **`down` method:** Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback. The column is nullable because existing rows will not have values after the column is re-added, and the original data is lost after the `up` migration.

3. **Local `Advisory` enum:** Defines a local `Iden` enum for `Advisory::Table` and `Advisory::Status` within the migration module. This is preferred over importing from the entity crate because:
   - The entity no longer has a `Status` variant (it was already removed)
   - Migrations should be self-contained and not depend on the current state of entity definitions, which may change over time

4. **Documentation comment:** Added a doc comment on the `Migration` struct explaining why this migration exists, per the code quality practices in the skill definition (Step 6).

## Convention Compliance

- **Trait implementation:** Implements `MigrationTrait` with both `up` and `down` methods, matching the `m0001_initial` pattern.
- **Derive macro:** Uses `#[derive(DeriveMigrationName)]` consistent with the sibling migration.
- **Async trait:** Uses `#[async_trait::async_trait]` attribute consistent with SeaORM migration patterns.
- **Return type:** Both methods return `Result<(), DbErr>` as required by the trait contract.
- **Module structure:** Placed in `migration/src/m0002_drop_advisory_status/mod.rs` following the `m<NNNN>_<description>/mod.rs` naming convention.

## Acceptance Criteria Coverage

| Criterion | How Addressed |
|---|---|
| Migration drops the `status` column | `up` method calls `drop_column(Advisory::Status)` |
| `down` method re-adds as nullable string | `down` method uses `ColumnDef::new(Advisory::Status).string().null()` |
| Migration is registered in lib.rs | Covered by File 1 changes |
| No service/entity code references status | Verified during pre-implementation grep (not a file change) |
