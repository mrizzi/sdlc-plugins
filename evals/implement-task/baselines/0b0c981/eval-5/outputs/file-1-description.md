# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file would be created following the pattern discovered in the sibling migration `migration/src/m0001_initial/mod.rs`.

### Structure

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

/// Identifiers for the advisory table and its columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`up()` method**: Uses `TableAlterStatement` via `Table::alter()` to drop the `Status` column from the `Advisory` table, exactly as specified in the Implementation Notes.

2. **`down()` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- a nullable string column. This matches the original column type and allows rollback without data loss concerns (the column data was discarded during the `up` migration, so the re-added column will be empty).

3. **`Advisory` enum**: A local `DeriveIden` enum is defined within this migration module to reference the table and column names. This is standard SeaORM migration practice -- each migration defines its own identifier enums to remain self-contained and not depend on entity definitions that may change over time.

4. **`DeriveMigrationName`**: The struct uses SeaORM's `DeriveMigrationName` derive macro, which automatically generates the migration name from the module path (e.g., `m0002_drop_advisory_status`).

### Conventions Applied

- Follows the same import style as `m0001_initial` (using `sea_orm_migration::prelude::*`)
- Follows the same `MigrationTrait` implementation pattern with `up()` and `down()`
- Follows the same error handling (returning `Result<(), DbErr>`, propagating with `.await`)
- Includes documentation comment on the `Advisory` enum explaining its purpose
- Module directory name follows the `m<NNNN>_<description>` naming pattern established by `m0001_initial`
- Uses `#[async_trait::async_trait]` attribute consistent with sibling migration
