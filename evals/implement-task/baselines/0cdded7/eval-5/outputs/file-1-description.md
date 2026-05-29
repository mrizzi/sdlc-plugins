# File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the pattern established by the existing `m0001_initial` migration.

## Pre-implementation inspection

Before writing this file, read `migration/src/m0001_initial/mod.rs` to confirm the exact pattern for:
- Import statements (which SeaORM migration prelude items are used)
- The migration struct name and how `MigrationName` trait is implemented
- The `up` and `down` method signatures and return types
- How `SchemaManager` methods are called

Also read `entity/src/advisory.rs` to:
- Verify the `status` column is NOT present in the entity's `Column` enum or `Model` struct
- Confirm that the `Advisory` enum has a `Table` variant for referencing the table name
- Understand the column naming pattern (e.g., whether there is a `Status` variant that was previously used)

## Detailed Changes

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

/// Identifiers for the advisory table and columns used in this migration.
#[derive(DeriveIden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`DeriveMigrationName`**: Uses the derive macro to automatically generate the migration name from the module path, consistent with `m0001_initial`.

2. **`Advisory` enum local to migration**: Defines a local `Advisory` enum with `DeriveIden` containing only `Table` and `Status` variants. This is the standard SeaORM migration pattern -- migrations define their own identifier enums rather than importing from the entity crate, ensuring migrations remain self-contained and stable even if entities change later.

3. **`up` method**: Uses `Table::alter()` with `drop_column(Advisory::Status)` to remove the column. This generates the SQL `ALTER TABLE advisory DROP COLUMN status`.

4. **`down` method**: Re-adds the column as `string().null()` (nullable VARCHAR/TEXT) to allow rollback. The column is nullable because existing rows will not have data for it after rollback.

5. **No data migration**: Since the task states the column is no longer read or written by any service code, no data preservation or transformation is needed.
