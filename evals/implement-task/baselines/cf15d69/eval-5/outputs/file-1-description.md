# File 1: CREATE `migration/src/m0002_drop_advisory_status/mod.rs`

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the existing migration pattern established by `m0001_initial/mod.rs`.

## Detailed Changes

### Structure

The file implements a SeaORM migration with the standard `MigrationTrait` pattern:

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer referenced by any entity or service code.
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

    /// Re-adds the `status` column as a nullable string to allow rollback.
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

/// Identifiers for the advisory table and its columns, used by SeaORM's
/// query builder for type-safe table/column references.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Decisions

1. **Struct naming**: `Migration` -- follows the convention from `m0001_initial/mod.rs` where the migration struct is simply named `Migration` (each module has its own namespace).

2. **`Iden` enum**: A local `Advisory` enum with `Table` and `Status` variants is defined in this module to reference the table and column in a type-safe manner. This avoids importing from the entity crate (which no longer has the `Status` field) and follows the self-contained migration pattern.

3. **`up()` method**: Uses `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)` as specified in the Implementation Notes. This generates an `ALTER TABLE advisory DROP COLUMN status` SQL statement.

4. **`down()` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- a nullable string column -- allowing safe rollback without data loss concerns (the column data is already gone after `up()` runs).

5. **`name()` method**: Returns `"m0002_drop_advisory_status"` matching the module directory name, following the naming convention from `m0001_initial`.

6. **Documentation**: Every public item has a `///` doc comment explaining its purpose, as required by the skill's code quality practices.

### Pre-implementation Verification

Before creating this file, the following would be verified:

- Inspect `m0001_initial/mod.rs` to confirm the exact pattern (struct name, trait implementation, import style)
- Inspect `entity/src/advisory.rs` to confirm `Status` is NOT in the entity definition
- Search the entire codebase for references to `Advisory::Status`, `status` column, or related query patterns to confirm nothing depends on the column
- Check if `Advisory` Iden enum exists elsewhere or if a local one is needed

### Conventions Applied

- Same module structure as `m0001_initial` (single `mod.rs` file in a named directory)
- Same import pattern (SeaORM migration prelude)
- Same struct naming (`Migration`)
- Same trait implementation order (`MigrationName`, then `MigrationTrait`)
- SeaORM's `TableAlterStatement` API for schema changes
