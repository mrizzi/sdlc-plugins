# File 1: migration/src/m0002_drop_advisory_status/mod.rs (CREATE)

## Purpose

New SeaORM migration that drops the deprecated `status` column from the `advisory` table.

## Detailed Changes

This file is created following the pattern discovered in `migration/src/m0001_initial/mod.rs`.

### Structure

- **Imports**: Import `sea_orm_migration::prelude::*` and reference the `Advisory` entity enum for table/column identifiers (following the pattern from m0001_initial).

- **Migration struct**: Define a unit struct `Migration` that implements `MigrationTrait`.

- **`name()` method**: Return the migration identifier string, following the naming convention from the existing migration (e.g., `"m0002_drop_advisory_status"`).

- **`up()` method**: Drop the `status` column from the `advisory` table using SeaORM's `TableAlterStatement`:
  ```rust
  manager
      .alter_table(
          Table::alter()
              .table(Advisory::Table)
              .drop_column(Advisory::Status)
              .to_owned(),
      )
      .await
  ```

- **`down()` method**: Re-add the column as a nullable string to support rollback:
  ```rust
  manager
      .alter_table(
          Table::alter()
              .table(Advisory::Table)
              .add_column(ColumnDef::new(Advisory::Status).string().null())
              .to_owned(),
      )
      .await
  ```

- **Entity enum reference**: Either import the `Advisory` enum from the entity crate or define a local `Advisory` enum with `Table` and `Status` variants (following whatever pattern m0001_initial uses for referencing table/column identifiers).

## Conventions Applied

- Follows the `MigrationTrait` implementation pattern from `m0001_initial/mod.rs`
- Uses SeaORM's schema alteration API consistently with the existing codebase
- Provides a reversible migration with both `up` and `down` methods
- Module naming follows the `m{number}_{description}` convention
