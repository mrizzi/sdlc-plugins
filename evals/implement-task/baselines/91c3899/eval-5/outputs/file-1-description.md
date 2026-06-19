# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. This follows the established migration pattern from `migration/src/m0001_initial/mod.rs`.

## Detailed Implementation

The file implements `MigrationTrait` for a new struct `Migration` with three required methods:

### Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration that drops the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
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

/// Enum representing the `advisory` table and its columns for SeaORM migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **Follows sibling pattern**: The structure mirrors `m0001_initial/mod.rs` exactly -- same imports, same trait implementation, same `Iden` enum pattern for table/column references.

2. **`up()` method**: Uses `TableAlterStatement` with `drop_column(Advisory::Status)` as specified in the Implementation Notes. This is the standard SeaORM approach for altering tables.

3. **`down()` method**: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` -- making it nullable so that existing rows don't fail on rollback (they will have NULL for the status column, which is acceptable since the column is deprecated).

4. **`Advisory` Iden enum**: Defined locally within the migration module (not imported from the entity crate) to keep the migration self-contained and immune to future entity changes. This follows SeaORM migration best practices.

5. **Documentation**: Every public symbol and method has a doc comment per the skill's code quality requirements.

### Conventions Applied

- Module naming: `m<NNNN>_<descriptive_name>` pattern (m0002_drop_advisory_status)
- File location: `migration/src/m0002_drop_advisory_status/mod.rs` (directory-based module)
- Trait implementation: `MigrationName` + `MigrationTrait` with `name()`, `up()`, `down()`
- Error type: Returns `Result<(), DbErr>` (SeaORM standard)
- Column identifiers: Uses local `Iden` enum, not entity crate imports
