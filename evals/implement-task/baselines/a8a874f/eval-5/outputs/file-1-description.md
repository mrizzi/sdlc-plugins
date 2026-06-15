# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the pattern established by the existing `m0001_initial` migration.

## Detailed Implementation

The file implements `MigrationTrait` for a `Migration` struct with two methods:

### Imports

```rust
use sea_orm_migration::prelude::*;
```

This matches the standard SeaORM migration import pattern.

### Enum Definition

Define an enum for referencing the advisory table and its columns, following SeaORM conventions:

```rust
#[derive(Iden)]
enum Advisory {
    Table,
    Status,
}
```

This allows the migration to reference `Advisory::Table` and `Advisory::Status` in a type-safe way via `TableAlterStatement`.

### Migration Struct

```rust
#[derive(DeriveMigrationName)]
pub struct Migration;
```

The `DeriveMigrationName` derive macro generates the migration name from the module path, which includes the `m0002_drop_advisory_status` directory name.

### MigrationTrait Implementation

```rust
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
```

### Method Details

- **`up()`**: Uses `Table::alter()` to build a `TableAlterStatement` that drops the `status` column from the `advisory` table. This is the exact pattern specified in the Implementation Notes: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`

- **`down()`**: Re-adds the `status` column as a nullable string (`ColumnDef::new(Advisory::Status).string().null()`) to allow rollback. The column is nullable because existing rows will have no value for this column after rollback. This matches the Implementation Notes specification.

### Convention Conformance

- Follows the same module structure as `m0001_initial/mod.rs` (sibling migration)
- Uses `DeriveMigrationName` macro for consistent naming
- Implements both `up` and `down` methods for reversibility (MigrationTrait contract)
- Uses SeaORM's `TableAlterStatement` builder API (not raw SQL)
- Enum-based column references (type-safe, matches SeaORM patterns)

### Documentation

The file would include a doc comment at the module level:

```rust
//! Migration to drop the deprecated `status` column from the `advisory` table.
//!
//! The `status` column was replaced by the `severity` enum field in a previous
//! migration (m0001_initial) and is no longer read or written by any service code.
```
