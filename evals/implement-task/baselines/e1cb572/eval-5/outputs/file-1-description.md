# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file implements the `MigrationTrait` from SeaORM, following the exact pattern established by the sibling migration `m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
/// Removing it reduces confusion and prevents accidental usage.
pub struct Migration;

impl MigrationName for Migration {
    fn name(&self) -> &str {
        "m0002_drop_advisory_status"
    }
}

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

    /// Re-adds the `status` column as a nullable string for rollback support.
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

/// Iden enum for referencing the advisory table and its columns in SeaORM migrations.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Decisions

1. **Follows sibling pattern**: The structure mirrors `m0001_initial/mod.rs` exactly -- implementing `MigrationName` and `MigrationTrait` with `up` and `down` methods.
2. **Uses `TableAlterStatement`**: As specified in the Implementation Notes, uses `Table::alter()` to drop the column rather than raw SQL.
3. **Rollback support**: The `down` method re-adds the column as `string().null()` (nullable string), allowing safe rollback without data loss expectations.
4. **Local `Iden` enum**: Defines a local `Advisory` enum with `Table` and `Status` variants for type-safe column references, following SeaORM migration conventions.
5. **Documentation comments**: Every public symbol and method has a `///` doc comment explaining its purpose.

### Conventions Applied

- **Error handling**: Returns `Result<(), DbErr>` as required by the `MigrationTrait` contract.
- **Naming**: Migration module follows the `m<NNNN>_<description>` directory naming pattern established by `m0001_initial`.
- **Async trait**: Uses `#[async_trait::async_trait]` attribute as required by SeaORM's `MigrationTrait`.
