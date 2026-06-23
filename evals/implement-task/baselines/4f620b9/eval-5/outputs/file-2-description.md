# File 2: migration/src/m0002_drop_advisory_status/mod.rs (Create)

## Purpose

New migration that drops the deprecated `status` column from the `advisory` table. The `down` method re-adds the column as a nullable string to support rollback.

## Full File Content

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration and is no longer read or written by any service code. Removing it
//! reduces confusion and prevents accidental usage.

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

/// Identifiers for the `advisory` table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Design Decisions

1. **`DeriveMigrationName` macro**: Automatically derives the migration name from the module path (`m0002_drop_advisory_status`), consistent with the pattern in `m0001_initial`.

2. **`up` method**: Uses `TableAlterStatement` via `Table::alter()` to drop the `status` column, as specified in the Implementation Notes. This is the standard SeaORM approach for column removal.

3. **`down` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback. The column is nullable because existing rows will not have a value for it after rollback. This matches the Implementation Notes specification.

4. **Local `Advisory` enum**: Defines a local `DeriveIden` enum for table and column identifiers rather than importing from the entity crate. This is standard practice for migrations because:
   - The entity module may have already removed the `Status` variant (as noted in the task: "the advisory entity no longer references the status column").
   - Migrations must be self-contained and not break if entity definitions change in the future.

5. **Documentation**: Module-level doc comment explains the purpose. Doc comments on `up` and `down` methods describe what each direction does.

## Conventions Followed

- Follows the same structure as `m0001_initial/mod.rs`: struct `Migration`, `MigrationTrait` implementation with `up` and `down`, local `DeriveIden` enum.
- Uses `sea_orm_migration::prelude::*` for imports.
- Uses `async_trait` for the async trait implementation.
- Both `up` and `down` return `Result<(), DbErr>`.
