# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Implementation

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code. Removing it
//! reduces confusion and prevents accidental usage.

use sea_orm_migration::prelude::*;

/// Migration that drops the `status` column from the `advisory` table.
#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the deprecated `status` column from the `advisory` table.
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

    /// Re-adds the `status` column as a nullable string for rollback safety.
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

- Follows the same module structure as `m0001_initial/mod.rs` (unit struct `Migration`, `MigrationTrait` impl)
- Uses `DeriveMigrationName` derive macro for automatic name generation from the module path
- Uses `DeriveIden` for the table/column identifier enum, scoped locally to this migration
- Both `up()` and `down()` return `Result<(), DbErr>` via the `SchemaManager`
- Uses SeaORM's builder pattern for `TableAlterStatement`
- The `down()` method re-adds the column as `.string().null()` to match the original column type while allowing rollback without data loss
- Documentation comments on the module, struct, and both methods
