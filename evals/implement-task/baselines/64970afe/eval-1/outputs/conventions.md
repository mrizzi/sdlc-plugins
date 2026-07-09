# Discovered Conventions (from sibling analysis)

## Step 0 -- Validate Project Configuration

The project CLAUDE.md (`claude-md-mock.md`) contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`)
3. **Code Intelligence** -- present, documents tool naming convention `mcp__<serena-instance>__<tool>` and lists `serena_backend` with `rust-analyzer`

All prerequisites satisfied. Proceeding.

## CONVENTIONS.md Lookup

The repository structure lists a `CONVENTIONS.md` at the repository root (`trustify-backend/CONVENTIONS.md`). In a real execution, this file would be read via `mcp__serena_backend__read_file` or the Read tool. Any CI check commands, code generation commands, naming rules, and project-wide conventions found there would be recorded and followed throughout implementation.

## Production Code Conventions (from sibling analysis)

### Service layer conventions (from `modules/fundamental/src/advisory/service/advisory.rs` siblings)

Sibling files inspected:
- `modules/fundamental/src/sbom/service/sbom.rs` (SbomService)
- `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService -- the target file itself)

Discovered patterns:
- **Method signatures**: Service methods take `&self`, entity-specific ID parameters, and `tx: &Transactional<'_>` as the last parameter. Example: `fetch(&self, id: Id, tx: &Transactional<'_>)`, `list(&self, ...)`.
- **Return types**: All service methods return `Result<T, AppError>` where `T` is a model struct.
- **Error handling**: Errors are wrapped using `.context("descriptive message")` before propagating with `?`.
- **Naming**: Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`). The new method should be named `severity_summary` following this pattern.
- **Database access**: Services use SeaORM entity queries. Join operations use the entity module's structs (e.g., `entity::sbom_advisory`).

### Endpoint conventions (from `modules/fundamental/src/advisory/endpoints/` siblings)

Sibling files inspected:
- `modules/fundamental/src/advisory/endpoints/get.rs` (GET /api/v2/advisory/{id})
- `modules/fundamental/src/advisory/endpoints/list.rs` (GET /api/v2/advisory)
- `modules/fundamental/src/sbom/endpoints/get.rs` (GET /api/v2/sbom/{id})

Discovered patterns:
- **Path extraction**: Handlers use `Path<Id>` from Axum to extract path parameters.
- **Handler signature**: `async fn handler_name(Path(id): Path<Id>, State(state): State<AppState>) -> Result<Json<T>, AppError>`
- **Service invocation**: Handlers call the service via `state.service.method(id, &Transactional::None).await?` or similar.
- **Response type**: Handlers return the struct directly via Axum's `Json<T>` extractor -- no manual serialization needed.
- **Error handling**: Handlers use `Result<T, AppError>` with `.context()` wrapping, matching `common/src/error.rs`.
- **Route registration**: In `endpoints/mod.rs`, routes are registered using `Router::new().route("/path", get(handler))` chains.

### Model conventions (from `modules/fundamental/src/advisory/model/` siblings)

Sibling files inspected:
- `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary)
- `modules/fundamental/src/advisory/model/details.rs` (AdvisoryDetails)
- `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary)

Discovered patterns:
- **Derive macros**: All model structs derive `Serialize, Deserialize, Clone, Debug` (and possibly `utoipa::ToSchema` for OpenAPI generation).
- **Module registration**: Each model file is registered in its parent `mod.rs` with `pub mod <name>;`.
- **Field types**: Numeric counts use `i64` or `usize`. IDs use the project's `Id` type.
- **Struct naming**: Structs use PascalCase with a domain-specific prefix (e.g., `AdvisorySummary`, `SbomSummary`).
- **AdvisorySummary has a `severity` field**: This confirms the existence of severity data on advisories, which the new `severity_summary` method will aggregate.

### Import organization conventions

- Standard library imports first, then external crate imports, then internal module imports.
- Each group is separated by a blank line.

## Test Conventions (from sibling test analysis)

Sibling test files inspected:
- `tests/api/advisory.rs` (Advisory endpoint integration tests)
- `tests/api/sbom.rs` (SBOM endpoint integration tests)
- `tests/api/search.rs` (Search endpoint integration tests)

Discovered patterns:
- **Assertion style**: All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` (or `StatusCode::NOT_FOUND` for 404 cases) followed by body deserialization via `resp.json::<T>().await`.
- **Response validation**: Tests validate specific field values in the response body, not just status codes.
- **Error cases**: All endpoint test files include at least one test for non-existent resource returning 404.
- **Test naming**: Tests follow `test_<endpoint_action>_<scenario>` pattern (e.g., `test_get_advisory_not_found`, `test_list_sboms_filtered`).
- **Test setup**: Integration tests use a real PostgreSQL test database with test fixtures seeded before assertions.
- **Given-When-Then**: Following the SKILL.md requirement, all new tests will include `// Given`, `// When`, `// Then` section comments even if siblings do not.
- **Documentation**: Following the SKILL.md requirement, every new test function will have a `///` doc comment explaining what it verifies.
- **Parameterized tests**: Sibling tests do not appear to use `#[rstest]` or parameterized patterns -- individual test functions are used for each scenario. We will follow this existing convention.

## Convention Conflicts

No conflicts detected between the task description / Implementation Notes and the discovered conventions. The task explicitly references the same patterns found in sibling analysis (e.g., `Path<Id>`, `Result<T, AppError>`, `.context()` wrapping, `Router::new().route()` registration).
