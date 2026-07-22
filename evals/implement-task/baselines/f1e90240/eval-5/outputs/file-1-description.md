# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file is created from scratch, following the pattern established by the sibling migration `migration/src/m0001_initial/mod.rs`.

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
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

/// Enum for referencing the `advisory` table and its columns in SeaORM statements.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`#[derive(DeriveMigrationName)]`**: Follows the SeaORM convention for automatic migration naming based on the module path.

2. **`Advisory` enum with `#[derive(Iden)]`**: Defines identifiers for the table and column names used in the alter statements. This is scoped locally to this migration module (not imported from the entity crate) to keep migrations self-contained and independent of entity changes.

3. **`up` method**: Uses `Table::alter().drop_column()` as specified in the Implementation Notes. This produces a `ALTER TABLE advisory DROP COLUMN status` SQL statement.

4. **`down` method**: Re-adds the column as `.string().null()` -- a nullable string column. This matches the original column type and allows rollback without data loss concerns (since the column is already deprecated and not populated by current code).

5. **Documentation comments**: Every public symbol (struct, methods, enum) has a `///` doc comment explaining its purpose, following the skill's code quality practices requirement.

### Conventions Followed

- Implements `MigrationTrait` with both `up` and `down` methods (matching `m0001_initial` pattern)
- Uses `sea_orm_migration::prelude::*` import (matching sibling)
- Uses `async_trait` for the async trait implementation (matching sibling)
- Returns `Result<(), DbErr>` from both migration methods (matching sibling)
- Defines a local `Iden` enum for table/column references (standard SeaORM migration pattern)
