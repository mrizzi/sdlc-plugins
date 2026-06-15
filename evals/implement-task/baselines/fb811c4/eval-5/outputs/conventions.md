# Discovered Conventions

## Conventions from CONVENTIONS.md

The repository tree lists a `CONVENTIONS.md` at the root. Since we cannot read it in this eval, we note its existence and would read it in a real implementation.

## Discovered Conventions (from sibling analysis)

### Migration Conventions (from `migration/src/m0001_initial/mod.rs`)

- **Module pattern:** Each migration lives in its own subdirectory under `migration/src/` named with a sequential prefix (e.g., `m0001_initial`, `m0002_drop_advisory_status`).
- **File structure:** Each migration directory contains a single `mod.rs` file.
- **Trait implementation:** Each migration implements `MigrationTrait` with `up` and `down` methods.
- **Registration:** Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function.
- **Module declaration:** Each migration module is declared with `mod m000N_...;` in `migration/src/lib.rs`.
- **Framework:** SeaORM migration framework is used (`sea_orm_migration::prelude::*`).

### Entity Conventions (from `entity/src/advisory.rs`)

- **ORM:** SeaORM is used for entity definitions.
- **Entity structure:** Each entity has its own file under `entity/src/`.
- **Column enum:** Entity columns are defined as enum variants (e.g., `Advisory::Table`, `Advisory::Status`).
- **Verification:** The `advisory.rs` entity no longer references the `status` column (as stated in the task), meaning the column enum variant for `Status` may already be removed or should not be present.

### General Code Conventions

- **Framework:** Axum for HTTP, SeaORM for database.
- **Error handling:** All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Module pattern:** Each domain module follows `model/ + service/ + endpoints/` structure.
- **Response types:** List endpoints return `PaginatedResults<T>`.
- **Testing:** Integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

### Test Conventions

- **Location:** Integration tests in `tests/api/` directory.
- **Test database:** Tests run against a real PostgreSQL test database.
- **Assertion style:** `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks.
- **Test file naming:** Tests are named after the domain they test (e.g., `advisory.rs`, `sbom.rs`).
