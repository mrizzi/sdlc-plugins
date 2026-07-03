# File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

## Action: CREATE

## Purpose

New SeaORM migration module that drops the deprecated `status` column from the `advisory` table. This is a DDL-only migration with no data transformation.

## Detailed Changes

### Imports

```rust
use sea_orm_migration::prelude::*;
```

### Struct definition

```rust
/// Migration to drop the deprecated `status` column from the `advisory` table.
///
/// The `status` column was replaced by the `severity` enum field in a previous
/// migration (m0001_initial) and is no longer read or written by any service code.
#[derive(DeriveMigrationName)]
pub struct Migration;
```

### MigrationTrait implementation

```rust
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

## Conventions followed

- Same module structure as `m0001_initial/mod.rs` (struct + MigrationTrait impl)
- Uses `#[derive(DeriveMigrationName)]` for automatic migration name derivation
- Both `up` and `down` methods implemented for reversibility
- `down` re-adds column as nullable string (`.string().null()`) so rollback does not break existing rows
- Local `Iden` enum for table/column references, following SeaORM conventions
- Documentation comments on the struct and both methods

## Acceptance criteria addressed

- Migration drops the `status` column from the `advisory` table (via `up` method)
- Migration `down` method re-adds the column as nullable string for rollback
