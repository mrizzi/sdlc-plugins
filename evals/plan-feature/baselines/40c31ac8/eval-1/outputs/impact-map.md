# Impact Map — TC-9001: Add advisory severity aggregation endpoint

**Workflow Mode:** direct-to-main

## Repository: trustify-backend

### New Files
| File | Purpose |
|---|---|
| `modules/fundamental/src/sbom/model/advisory_summary.rs` | `AdvisorySeveritySummary` response struct with fields: critical, high, medium, low, total (all i64), derives Serialize/Deserialize/Debug/Clone |
| `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` | Async handler for `GET /api/v2/sbom/{id}/advisory-summary`; extracts SBOM ID from path, optional `threshold` from query params; calls `SbomService::get_advisory_summary()`; returns `Json<AdvisorySeveritySummary>` with 5-minute cache header |
| `tests/api/sbom_advisory_summary.rs` | Integration tests for the advisory-summary endpoint covering: valid SBOM response, 404 for missing SBOM, empty advisory set, threshold filtering, advisory deduplication, cache header verification |

### Modified Files
| File | Change |
|---|---|
| `modules/fundamental/src/sbom/model/mod.rs` | Add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary` |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add `get_advisory_summary(&self, sbom_id: Uuid, threshold: Option<String>) -> Result<AdvisorySeveritySummary, AppError>` method; joins `sbom_advisory` with `advisory` entity, groups by severity, counts distinct advisory IDs, verifies SBOM existence (404 if missing), applies optional threshold filter |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register route `.route("/api/v2/sbom/:id/advisory-summary", get(advisory_summary::handler))` with tower-http CacheControl layer (max_age=300) |
| `modules/ingestor/src/graph/advisory/mod.rs` | Add cache invalidation after advisory-to-SBOM correlation step; evict cached advisory-summary for each affected SBOM ID when new `sbom_advisory` records are inserted |

### API Changes
| Method | Path | Change |
|---|---|---|
| GET | `/api/v2/sbom/{id}/advisory-summary` | NEW: Returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` with `Cache-Control: max-age=300`; optional `?threshold=critical\|high\|medium\|low` query parameter filters to severities at or above the threshold |

### Entity References (no schema changes)
| Entity File | Usage |
|---|---|
| `entity/src/sbom.rs` | Read: verify SBOM existence by ID |
| `entity/src/advisory.rs` | Read: access severity field for grouping |
| `entity/src/sbom_advisory.rs` | Read: join table for SBOM-advisory relationships, used for aggregation query and deduplication |

### Task Dependency Graph
```
Task 1 (model) --> Task 2 (service) --> Task 3 (endpoint) --> Task 4 (threshold)
                                                |                     |
                                                v                     v
                                          Task 5 (cache inv.)   Task 6 (tests)
                                                |                     ^
                                                +---------------------+
```

### Rationale - Workflow Mode
**Selected mode:** direct-to-main
No atomicity indicators: purely additive endpoint, no schema migrations, no breaking API changes, single repository.
