# File 1: migration/src/m0002_drop_advisory_status/mod.rs

## Action: CREATE

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Pre-implementation Inspection

Before writing this file, inspect `migration/src/m0001_initial/mod.rs` to confirm:
- The exact import statements used (e.g., `sea_orm_migration::prelude::*`)
- How `MigrationTrait` is implemented (struct name, `name()` return format, async `up`/`down` signatures)
- How table/column identifiers are referenced (enum-based like `Advisory::Table` vs string-based)
- Whether the migration uses `Iden` derive macros for table/column enums

## Detailed Changes

The file should contain the following structure, adapted to match the exact patterns found in the sibling migration:

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
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

## Key Design Decisions

1. **`DeriveMigrationName`**: Uses the derive macro so the migration name is automatically derived from the module path (matching the `m0001_initial` convention).

2. **`Advisory` enum with `Iden` derive**: Defines only the table and column identifiers needed for this migration (`Table` and `Status`), rather than importing from the entity crate. This is a common SeaORM migration pattern -- migrations should be self-contained and not depend on entity definitions that may change over time.

3. **`down` method**: Re-adds `status` as a nullable string column (`string().null()`), matching the task requirement. This ensures rollback is safe even if existing rows have no value for this column.

4. **`up` method**: Drops the `status` column using `TableAlterStatement::drop_column`, matching the implementation note in the task description.

## Conventions to Confirm from Sibling

- If `m0001_initial/mod.rs` uses `#[derive(DeriveMigrationName)]` vs a manual `fn name()` implementation
- If `m0001_initial/mod.rs` uses `#[async_trait::async_trait]` or `#[async_trait]` with a use statement
- If table/column Iden enums are defined inline in the migration file or imported from elsewhere
- The exact formatting style (trailing commas, method chaining indentation)
