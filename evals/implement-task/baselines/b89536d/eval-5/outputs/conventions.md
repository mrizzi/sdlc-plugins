# Conventions Discovered from Sibling Analysis

## Source: Repository Key Conventions (from repo-backend.md)

- **Framework**: Axum for HTTP, SeaORM for database
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure
- **Error handling**: All handlers return `Result<T, AppError>` with `.context()` wrapping
- **Endpoint registration**: Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- **Response types**: List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Query helpers**: Shared filtering, pagination, and sorting via `common/src/db/query.rs`
- **Testing**: Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- **Caching**: Uses `tower-http` caching middleware; cache configuration in endpoint route builders

## Source: Migration Sibling Analysis (from m0001_initial)

The following conventions are inferred from the existing migration `m0001_initial/mod.rs`, which is the sole sibling migration:

- **Migration struct**: Each migration module defines a unit struct (e.g., `pub struct Migration;`) that implements `MigrationTrait`
- **MigrationName trait**: Each migration also implements `MigrationName` to provide a human-readable name for the migration
- **up/down pattern**: The `up` method applies the forward migration; the `down` method reverses it for rollback
- **SeaORM table operations**: Migrations use SeaORM's schema manager API (`manager.alter_table(...)`, `manager.create_table(...)`, etc.)
- **Module registration**: Migrations are registered in `migration/src/lib.rs` by:
  1. Adding a `mod <migration_name>;` declaration
  2. Adding `Box::new(<migration_name>::Migration)` to the `vec![]` returned by the `migrations()` function
- **Directory structure**: Each migration lives in its own subdirectory under `migration/src/` named with a prefix (e.g., `m0001_`, `m0002_`) followed by a descriptive name

## Source: Entity Analysis (from entity/src/advisory.rs)

- **Entity definition**: The advisory entity uses SeaORM derive macros and defines column enums
- **Column removal confirmation**: The `advisory.rs` entity no longer references a `status` column (it uses `severity` instead), confirming the column can be safely dropped at the database level

## Source: Test Sibling Analysis (from tests/api/)

- **Test location**: Integration tests for advisory operations live in `tests/api/advisory.rs`
- **Assertion style**: Tests use `assert_eq!(resp.status(), StatusCode::OK)` for status code checks
- **Database interaction**: Tests run against a real PostgreSQL test database
- **Test naming**: Tests follow `test_<action>_<scenario>` pattern

## CONVENTIONS.md

The repository includes a `CONVENTIONS.md` file at the root. In a real implementation, this file would be read and its conventions followed. Any CI check commands listed there would be extracted and run during Step 9 verification.
