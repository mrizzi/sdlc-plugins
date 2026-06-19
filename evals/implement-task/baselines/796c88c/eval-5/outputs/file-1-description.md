# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Detailed Changes

Create the file with the following implementation:

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code.

use sea_orm_migration::prelude::*;

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

    /// Re-adds the `status` column as a nullable string for rollback.
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

/// Identifiers for the `advisory` table and its columns used by this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Conventions Applied

- **Module structure:** Follows the `m<NNNN>_<description>/mod.rs` naming pattern established by `m0001_initial/mod.rs`
- **Trait implementation:** Implements `MigrationTrait` with both `up` and `down` methods, matching the sibling pattern
- **Derive macro:** Uses `DeriveMigrationName` to auto-generate the migration name from the module path
- **Iden enum:** Defines a local `Advisory` enum with `DeriveIden` for type-safe table/column references, following SeaORM conventions
- **Documentation:** Every public symbol has a doc comment using `///` (Rust convention)
- **Module-level doc:** `//!` doc comment at the top of the file explaining the migration's purpose
- **Async trait:** Uses `#[async_trait::async_trait]` for the async trait implementation, matching the sibling pattern
- **Error handling:** Returns `Result<(), DbErr>` as required by `MigrationTrait`

## Key Implementation Details

- The `up` method uses `Table::alter().drop_column()` via SeaORM's `TableAlterStatement` to drop the column
- The `down` method re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- nullable string allows rollback without data loss concerns
- The `Advisory` iden enum is local to this migration module (not imported from the entity crate) to avoid coupling migrations to entity definitions that may change over time
