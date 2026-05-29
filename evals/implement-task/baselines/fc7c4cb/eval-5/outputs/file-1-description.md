# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New SeaORM migration that drops the deprecated `status` column from the `advisory` table.

## Reference Files Inspected

- **`migration/src/m0001_initial/mod.rs`** -- the existing migration, used as the pattern
  template. This file implements `MigrationTrait` with `up` and `down` methods, defines
  a `Migration` struct, and uses SeaORM's schema management utilities.
- **`entity/src/advisory.rs`** -- the Advisory entity definition. Verified that it no
  longer references a `Status` column, confirming the column is safe to drop.

## Detailed Changes

The file implements the following structure, mirroring the pattern in `m0001_initial/mod.rs`:

### Module-level imports

```rust
use sea_orm_migration::prelude::*;
```

Following the import pattern from `m0001_initial/mod.rs`.

### Migration struct

```rust
/// Migration to drop the deprecated `status` column from the `advisory` table.
#[derive(DeriveMigrationName)]
pub struct Migration;
```

### Iden enum for table/column references

```rust
/// Identifiers for the advisory table and its columns used in this migration.
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

This enum provides type-safe references to the table and column names, following
the SeaORM convention seen in `m0001_initial/mod.rs`.

### MigrationTrait implementation

```rust
#[async_trait::async_trait]
impl MigrationTrait for Migration {
    /// Drops the deprecated `status` column from the `advisory` table.
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
```

### Key design decisions

1. **`up` method**: Uses `TableAlterStatement` with `drop_column` as specified in the
   Implementation Notes. This is a non-reversible data operation (column data is lost).

2. **`down` method**: Re-adds the column as `string().null()` to allow rollback. The
   column is nullable because after dropping, there is no data to restore -- existing
   rows will have NULL for the re-added column.

3. **Iden enum**: Defines only `Table` and `Status` variants (the minimum needed for
   this migration), rather than listing all advisory columns.

4. **Documentation**: Every public symbol has a doc comment per the skill's code quality
   practices requirement.
