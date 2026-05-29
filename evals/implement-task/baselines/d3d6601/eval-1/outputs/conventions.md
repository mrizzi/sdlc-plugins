# Discovered Conventions from Sibling Analysis

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains all required sections:
1. **Repository Registry** -- present, maps `trustify-backend` to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present, tool naming convention `mcp__serena_backend__<tool>`, using rust-analyzer

## Step 1 -- Task Parsing

- **Repository**: trustify-backend
- **Target Branch**: main
- **Bookend Type**: none
- **Target PR**: none
- **GitHub Issue custom field**: customfield_10747 (configured but no value present on issue)
- **Dependencies**: None

## Step 1.5 -- Description Digest Verification

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`. If multiple match, select the most recent by `created` timestamp. If found, check `created` vs `updated` timestamps for edit detection, extract `sha256:<hex-digest>`, compute SHA-256 of current description, and compare. If no digest comment found, log warning and proceed: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Production Code Conventions (from sibling analysis)

### Module Structure
- Each domain module follows `model/ + service/ + endpoints/` structure
- Model modules have a `mod.rs` that re-exports sub-modules (e.g., `pub mod summary;`, `pub mod details;`)
- Service modules have a `mod.rs` that re-exports the main service file
- Endpoint modules have a `mod.rs` for route registration plus individual handler files

### Sibling files inspected
- **Model siblings**: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs`, `modules/fundamental/src/sbom/model/summary.rs`
- **Service siblings**: `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService with `fetch`, `list`, `search` methods)
- **Endpoint siblings**: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/sbom/endpoints/get.rs`

### Naming Conventions
- Service methods follow `verb_noun` pattern (e.g., `fetch`, `list`, `search`)
- Model structs use PascalCase domain names (e.g., `AdvisorySummary`, `SbomDetails`)
- Endpoint handler files named after HTTP action (e.g., `get.rs`, `list.rs`)
- Endpoint handler functions likely follow `get_<entity>`, `list_<entity>` pattern

### Error Handling
- All handlers return `Result<T, AppError>` with `.context()` wrapping for error details
- `AppError` enum defined in `common/src/error.rs`, implements `IntoResponse`

### Response Types
- Single-entity endpoints return the struct directly (via Axum's `Json` extractor)
- List endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The new severity_summary endpoint returns a single aggregate struct (not paginated)

### Route Registration
- Each module's `endpoints/mod.rs` registers routes using `Router::new().route("/path", get(handler))` pattern
- `server/main.rs` mounts all modules (no changes needed -- routes auto-mount via module registration)

### Framework Patterns
- **HTTP**: Axum -- path params extracted via `Path<Id>`, JSON responses via `Json<T>`
- **ORM**: SeaORM for database access
- **Caching**: tower-http caching middleware

### Import Organization
- Standard library imports first, then external crates, then internal modules (Rust convention)

## Test Conventions (from sibling test analysis)

### Sibling test files inspected
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- search endpoint integration tests

### Assertion Style
- All endpoint tests use `assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization
- Error cases use `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for 404 tests

### Test Naming
- Tests follow `test_<endpoint>_<scenario>` pattern (e.g., `test_list_advisories_filtered`)

### Test Structure
- Integration tests hit a real PostgreSQL test database
- Tests are organized by domain entity in `tests/api/` directory
- Each test file covers one entity type

### Test Setup
- Test database seeded with fixtures
- HTTP client sends requests to test server

### Documentation
- AI-generated tests must include `///` doc comments on every test function (per SKILL.md requirement)
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments

## CONVENTIONS.md Lookup

The repository has a `CONVENTIONS.md` at the root. Would read it for:
- CI check commands (formatting, linting, compilation) for Step 9 verification
- Code generation commands
- Any additional naming or structural conventions

## Documentation Files Identified

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (would need updating with the new endpoint)
