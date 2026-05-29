# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New SeaORM migration that drops the deprecated `status` column from the `advisory` table. This follows the pattern established by the existing migration in `migration/src/m0001_initial/mod.rs`.

## Pre-Implementation Inspection

Before creating this file, the following must be inspected:

1. **Read `migration/src/m0001_initial/mod.rs`** -- understand the exact `MigrationTrait` implementation pattern:
   - How `name()` returns the migration identifier
   - How `up()` and `down()` use the `SchemaManager` parameter
   - Import statements and module-level structure
   - Error handling (return type is `Result<(), DbErr>`)

2. **Read `entity/src/advisory.rs`** -- confirm the entity definition:
   - Verify `Advisory::Status` enum variant exists (needed for the `drop_column` call)
   - Verify the entity struct does NOT have a `status` field (confirming it was already removed)
   - Identify the `Advisory::Table` enum variant for table reference

## Detailed Changes

### Structure

The file implements `MigrationTrait` for a new `Migration` struct, following the `m0001_initial` pattern:

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

/// Enum representing the Advisory table and its columns for use in migrations.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

- **`up()` method:** Uses `TableAlterStatement` with `drop_column(Advisory::Status)` as specified in the Implementation Notes
- **`down()` method:** Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- nullable string to allow rollback without data loss
- **`Advisory` enum:** Local `Iden` enum for table/column references (standard SeaORM migration pattern -- must be verified against `m0001_initial` to confirm whether the project uses local enums or imports from the entity crate)
- **`DeriveMigrationName`:** Automatically derives the migration name from the module path

### Acceptance Criteria Coverage

- [x] Migration drops the `status` column from the `advisory` table (via `drop_column` in `up()`)
- [x] Migration `down` method re-adds the column as nullable string for rollback (via `add_column` with `.string().null()` in `down()`)
