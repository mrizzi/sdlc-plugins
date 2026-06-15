# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.
Follows the same pattern as the sibling migration `m0001_initial/mod.rs`.

## Detailed Changes

Create a new file with the following structure:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration and is no longer read or written by any service code.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the `status` column from the `advisory` table.
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

    /// Re-adds the `status` column as a nullable string to support rollback.
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

/// Enum identifying the `advisory` table and its columns for use in migration statements.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Applied

- **MigrationTrait implementation:** Follows the same `up`/`down` pattern as `m0001_initial/mod.rs`.
- **TableAlterStatement usage:** Uses `Table::alter()` with `.drop_column()` and `.add_column()`
  as specified in the Implementation Notes.
- **Rollback safety:** The `down` method re-adds the column as `.string().null()` to avoid
  NOT NULL constraint violations on existing rows.
- **Iden enum:** Defines a local `Advisory` enum with `DeriveIden` for type-safe table/column
  references, following SeaORM conventions.
- **Documentation comments:** Every public symbol has a `///` doc comment per the skill's
  code quality requirements.
- **Derive macro:** Uses `#[derive(DeriveMigrationName)]` to auto-generate the migration name
  from the module path, consistent with the existing migration.

## Verification

- Confirm `Advisory::Table` and `Advisory::Status` resolve correctly via the local `DeriveIden` enum.
- Confirm the `up` method drops the column and `down` re-adds it as nullable string.
- Run `cargo check` in the `migration` crate to verify compilation.
