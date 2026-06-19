# Discovered Conventions

## From CONVENTIONS.md

The repository includes a `CONVENTIONS.md` at the root. In this eval we cannot read its contents directly, but the repo structure document describes the key conventions.

## From Sibling Analysis

### Production Code Conventions

**Migration pattern (from `migration/src/m0001_initial/mod.rs`):**
- Each migration lives in its own module directory under `migration/src/` following the naming pattern `m<NNNN>_<description>/mod.rs`
- Migrations implement the `MigrationTrait` trait from SeaORM with `up` and `down` methods
- The `up` method applies the forward migration; `down` provides rollback capability
- Migrations are registered in `migration/src/lib.rs` by adding them to the `vec![]` returned by the `migrations()` function

**Framework conventions:**
- Framework: Axum for HTTP, SeaORM for database ORM
- Module pattern: each domain module follows `model/ + service/ + endpoints/` structure
- Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping
- Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules
- Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Query helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs`

**Entity conventions (from `entity/src/`):**
- SeaORM entities define table structure with column enums
- The `Advisory` entity in `entity/src/advisory.rs` uses column enums like `Advisory::Table`, `Advisory::Status`, `Advisory::Severity`
- The entity file no longer references the `status` column (per task description), confirming it is safe to drop

**Naming conventions:**
- Migration directories use snake_case with a numeric prefix: `m0001_initial`, `m0002_drop_advisory_status`
- Service methods follow `verb_noun` pattern (e.g., `get_advisory`, `create_sbom`)

### Test Conventions

**Testing patterns (from `tests/api/`):**
- Integration tests in `tests/api/` hit a real PostgreSQL test database
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code validation
- Test files are organized by domain entity: `sbom.rs`, `advisory.rs`, `search.rs`
- Test naming follows `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

**Migration test patterns:**
- Migration tests should verify that the migration runs successfully against a test database
- Rollback tests should verify the `down` method re-adds the dropped column
- Post-migration tests should verify existing queries still function correctly
