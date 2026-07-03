# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

Create a new file implementing the `MigrationTrait` following the pattern established in `m0001_initial/mod.rs`.

### Code Structure

```rust
use sea_orm_migration::prelude::*;

/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in migration m0001
/// and is no longer read or written by any service or entity code.
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

/// Enum referencing the `advisory` table and its columns for use in migration statements.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

### Key Design Decisions

1. **`Advisory` enum defined locally**: The migration defines its own `Advisory` enum with `Table` and `Status` variants rather than importing from the entity crate. This is a common SeaORM migration pattern because:
   - The entity module (`entity/src/advisory.rs`) no longer has a `Status` column (it was removed when `severity` was adopted)
   - Migrations must be self-contained and not depend on the current state of entity definitions
   - If the entity enum was used, future entity changes could break old migrations

2. **Nullable string in `down`**: The rollback re-adds `status` as `.string().null()` so that existing rows (which no longer have status values) don't violate a NOT NULL constraint.

3. **Documentation comments**: Every public symbol and both migration methods have `///` documentation comments per the skill's code quality requirements.
