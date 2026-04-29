# Discovered Conventions

## Conventions from CONVENTIONS.md (repository root)

The repository includes a `CONVENTIONS.md` file at the root. Its conventions should be followed (content not available in this simulated eval, but its existence is noted and would be read in a real implementation).

## Discovered conventions (from sibling analysis)

### Production code conventions

#### Module structure
- Each domain module follows the `model/ + service/ + endpoints/` directory structure (observed in `sbom/`, `advisory/`, `package/`).
- Model sub-modules are registered in `model/mod.rs` via `pub mod <name>;` declarations.
- Service files contain a service struct with methods like `fetch`, `list`, and domain-specific operations.
- Endpoint files are organized per-operation (e.g., `list.rs`, `get.rs`) with a `mod.rs` for route registration.

#### Endpoint patterns
- Endpoint handlers extract path parameters via `Path<Id>` (Axum extractor).
- All handlers return `Result<T, AppError>` with `.context()` wrapping for error propagation (pattern from `common/src/error.rs`).
- Route registration in `endpoints/mod.rs` uses `Router::new().route("/path", get(handler))` pattern.
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Single-item endpoints return the domain struct directly, serialized via Axum's `Json` extractor.
- Routes are auto-mounted by the server via module registration in `server/src/main.rs`.

#### Service patterns
- Service methods follow the `verb_noun` naming pattern (e.g., `fetch`, `list`, `search`).
- Service methods take `&self` as the first parameter and `tx: &Transactional<'_>` as the last parameter for database transaction context.
- Additional parameters (like entity IDs) are passed between `&self` and `tx`.

#### Error handling
- All error handling uses `Result<T, AppError>` with `.context()` wrapping.
- The `AppError` enum is defined in `common/src/error.rs` and implements `IntoResponse`.
- 404 errors should be returned when an entity is not found, consistent with existing SBOM endpoints.

#### Response types
- Model structs (e.g., `SbomSummary`, `AdvisorySummary`, `AdvisoryDetails`) are used as response types.
- Each struct has its own file in the `model/` directory.
- The `AdvisorySummary` struct includes a `severity` field that can be used for counting by severity level.

#### Database / ORM
- Framework: SeaORM for database access.
- Join tables exist for many-to-many relationships (e.g., `sbom_advisory.rs`, `sbom_package.rs`).
- Entities are defined in the `entity/` crate.

#### Naming conventions
- Files are named with snake_case matching the concept they contain (e.g., `severity_summary.rs` for `SeveritySummary`).
- Module directories match domain concepts (e.g., `advisory/`, `sbom/`, `package/`).

#### Import organization
- Crate-level imports from `common/` for shared types (`AppError`, `PaginatedResults`, query helpers).
- Entity imports from the `entity/` crate for ORM models.
- Axum imports for HTTP types (`Path`, `Json`, `Router`, `get`).

### Test conventions

#### Test file organization
- Integration tests live in `tests/api/` directory.
- Each domain has its own test file (e.g., `sbom.rs`, `advisory.rs`, `search.rs`).
- Tests hit a real PostgreSQL test database.

#### Assertion style
- Status code assertions use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Response bodies are deserialized and checked for specific field values.
- 404 tests use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)`.

#### Test naming
- Tests follow `test_<endpoint>_<scenario>` naming pattern (e.g., `test_list_advisories_filtered`).

#### Test structure
- Non-trivial tests should use given-when-then structure with `// Given`, `// When`, `// Then` section comments.
- Each test function should have a `///` documentation comment explaining what it verifies.

#### Error case coverage
- All endpoint test files include tests for 404 (non-existent entity) responses.
- Tests verify both success and error paths.
