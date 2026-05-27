# Conventions Discovered from Sibling Analysis

## Module Structure Convention
Each domain module (advisory, sbom, package) follows a consistent three-directory structure:
- `model/` — Data structs (summary, details) with Serde derive macros for serialization
- `service/` — Business logic structs with methods like `fetch`, `list`, `search`
- `endpoints/` — Axum HTTP handlers registered via `Router::new().route()`

The `model/mod.rs` file re-exports submodules with `pub mod <name>;` declarations.

## Endpoint Pattern (from `endpoints/get.rs` siblings)
- Path parameters extracted via Axum's `Path<Id>` extractor
- Service is injected (likely via Axum state/extension)
- Handler calls service method, returns `Result<Json<T>, AppError>`
- Routes registered in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))`

## Service Pattern (from `service/advisory.rs`)
- Service struct (e.g., `AdvisoryService`) with methods taking `&self`
- Methods accept domain-specific identifiers and a `tx: &Transactional<'_>` parameter for database transactions
- Methods return `Result<T, AppError>` where `T` is a model struct
- Error handling uses `.context("description")` wrapping from the `AppError` pattern in `common/src/error.rs`

## Model Pattern (from `model/summary.rs` siblings)
- Structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- `AdvisorySummary` struct includes a `severity` field that classifies advisory severity
- Response types for list endpoints use `PaginatedResults<T>` from `common/src/model/paginated.rs`

## Error Handling Convention
- All fallible operations return `Result<T, AppError>`
- `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`
- Errors are wrapped with `.context()` for descriptive messages
- 404 errors are used when resources are not found

## Database Convention
- SeaORM is used for database access
- Join tables (e.g., `sbom_advisory.rs` in `entity/src/`) link related entities
- Entity structs live in `entity/src/`

## Testing Convention
- Integration tests live in `tests/api/` directory
- Tests hit a real PostgreSQL database
- Test files are named after the domain they test (e.g., `sbom.rs`, `advisory.rs`)

## API Route Convention
- Routes follow the pattern `/api/v2/<resource>/{id}/<sub-resource>`
- The new endpoint follows this: `/api/v2/sbom/{id}/advisory-summary`

## Naming Convention
- File names use `snake_case`
- Struct names use `PascalCase`
- Method names use `snake_case`
- Module files use `snake_case`

## Commit Convention
- Conventional Commits format: `feat(module): description`
- Jira issue key included in commit footer
- Trailer: `Assisted-by: Claude Code`
