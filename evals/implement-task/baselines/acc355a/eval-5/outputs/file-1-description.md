# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Pre-implementation Inspection

Before creating this file, inspect:
- **`migration/src/m0001_initial/mod.rs`** — Read the full file to understand the migration pattern: struct definition, `MigrationTrait` implementation, `up()` and `down()` method signatures, use of `TableAlterStatement`, and how entity enum variants (e.g., `Advisory::Table`, `Advisory::Status`) are referenced.
- **`entity/src/advisory.rs`** — Verify that the `Advisory` entity enum still defines a `Status` variant (needed for the migration to reference it) or determine the correct way to reference the column if the variant has been removed.

## Detailed Changes

The file implements a SeaORM migration following the pattern in `m0001_initial/mod.rs`:

```rust
use sea_orm_migration::prelude::*;

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

#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`drop_column` in `up()`**: Uses SeaORM's `TableAlterStatement` to drop the column, matching the pattern from the task's Implementation Notes.

2. **`add_column` in `down()`**: Re-adds the column as `string().null()` to allow rollback. The column is nullable because existing rows won't have a value after rollback, and the column is deprecated anyway.

3. **Local `Iden` enum**: Defines a local `Advisory` enum with `Table` and `Status` variants for use in the migration. This follows the SeaORM migration convention of defining table/column identifiers locally rather than importing from the entity module (since the entity may have already removed the column reference).

## Conventions Applied

- Follow the exact struct and trait implementation pattern from `m0001_initial/mod.rs`
- Use `#[derive(DeriveMigrationName)]` for automatic migration name derivation
- Use `#[async_trait::async_trait]` for the async trait implementation
- Both `up()` and `down()` methods return `Result<(), DbErr>`
