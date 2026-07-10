# Conventions Discovered from Sibling Analysis

## Production Code Conventions

### Module Structure

- Each domain module follows the `model/ + service/ + endpoints/` directory structure
- Model module has `mod.rs` that declares submodules with `pub mod <name>;`
- Service module has `mod.rs` and a primary service file named after the domain (e.g., `advisory.rs`, `sbom.rs`)
- Endpoints module has `mod.rs` for route registration and separate files per handler (e.g., `get.rs`, `list.rs`)

### Error Handling

- All endpoint handlers return `Result<T, AppError>` where `AppError` is defined in `common/src/error.rs`
- Errors are wrapped using `.context()` for descriptive error messages
- `AppError` implements `IntoResponse` (Axum trait) for automatic HTTP error responses
- 404 errors returned when entity not found, consistent across all SBOM and advisory endpoints

### Naming Conventions

- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search` in `AdvisoryService`)
- Model structs follow `<Domain><Role>` pattern (e.g., `AdvisorySummary`, `AdvisoryDetails`, `SbomSummary`, `SbomDetails`)
- Endpoint files named by HTTP action: `get.rs`, `list.rs`
- New files for new features rather than appending to existing handler files

### Endpoint Patterns (from `advisory/endpoints/get.rs` and siblings)

- Path parameters extracted via Axum's `Path<Id>` extractor
- Service methods called with `(&self, id: Id, tx: &Transactional<'_>)` signature pattern
- Response returned as the struct directly -- Axum's `Json` extractor handles serialization
- Route registration in `endpoints/mod.rs` using `Router::new().route("/path", get(handler))` pattern

### Service Patterns (from `AdvisoryService` in `service/advisory.rs`)

- Service struct holds database connection/pool reference
- Methods take `&self` plus domain-specific parameters and a `tx: &Transactional<'_>` for transaction context
- `fetch` method: retrieves single entity by ID, returns Option or Result
- `list` method: retrieves paginated collection with filtering
- New methods added to the existing service impl block following the same pattern

### Model Patterns (from `advisory/model/summary.rs` and `details.rs`)

- Response structs derive `Serialize` (for JSON serialization) and likely `Clone`, `Debug`
- `AdvisorySummary` has a `severity` field -- this is the field used for counting severity levels
- Each model struct has its own file, declared in `model/mod.rs` via `pub mod <name>;`
- List endpoints use `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs`

### Entity/Database Patterns (from `entity/src/`)

- SeaORM used for database entities
- Join tables exist for many-to-many relationships (e.g., `sbom_advisory.rs` for SBOM-Advisory joins)
- Entity files at `entity/src/<name>.rs`

### Route Registration

- Each module's `endpoints/mod.rs` registers routes
- `server/main.rs` mounts all modules -- no changes needed there (auto-mount via module registration)
- Routes follow REST conventions: `/api/v2/<resource>` for lists, `/api/v2/<resource>/{id}` for single entities

### Import Organization

- Standard library imports first, then external crates, then internal modules
- Consistent with Rust convention (rustfmt ordering)

## Test Conventions

### Assertion Style

- Integration tests use `assert_eq!(resp.status(), StatusCode::OK)` for status checks
- Body deserialization follows status assertion
- `StatusCode::NOT_FOUND` for 404 tests

### Response Validation

- Tests validate response body structure by deserializing into the expected struct type
- Specific field values asserted rather than just presence
- Count-based assertions use `assert_eq!` with exact expected values

### Error Cases

- Every endpoint test suite includes a 404 test for non-existent entity IDs
- Error responses checked via `StatusCode::NOT_FOUND` assertion

### Test Naming

- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)
- Clear, descriptive names indicating what is being tested

### Test Setup

- Integration tests hit a real PostgreSQL test database
- Test fixtures created using service methods or direct database seeding
- Each test is self-contained with its own setup

### Test Organization

- Tests grouped by API domain area in `tests/api/` directory
- One file per domain area (e.g., `sbom.rs`, `advisory.rs`, `search.rs`)
- New test files declared in `tests/Cargo.toml` or test runner configuration

### Parameterized Tests

- Would check sibling tests for `#[rstest]` or `#[case]` usage
- If siblings do not use parameterized tests, do not introduce them
- Use individual test functions for each scenario as seen in sibling test files

### Test Documentation

- Per SKILL.md mandate, all test functions will have `///` doc comments regardless of sibling convention
- Non-trivial tests will include `// Given`, `// When`, `// Then` section comments
