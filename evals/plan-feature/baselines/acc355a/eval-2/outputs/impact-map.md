# Repository Impact Map — TC-9002: Improve Search Experience

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** All changes target a single repository (`trustify-backend`) and the search module. Each change (performance optimization, relevance tuning, filter support) can be merged independently without leaving `main` in a broken state. No coordinated schema migrations, no breaking cross-task API dependencies, and no cross-repo coupling were identified. No atomicity indicators are present.

## Ambiguities and Assumptions

The feature description (TC-9002) is intentionally vague in several areas. The following ambiguities were identified, with assumptions documented for each:

1. **"Search should be faster" — no latency target defined.**
   - Assumption: Optimize the existing `SearchService` full-text search by adding database indexing (GIN/GiST indexes for text columns) and query optimization. Target measurable improvement over current baseline, but no specific SLA is assumed.

2. **"Results should be more relevant" — no ranking criteria specified.**
   - Assumption: Implement basic search ranking using PostgreSQL `ts_rank` or equivalent scoring, and support multi-field search (search across SBOM names, advisory titles/descriptions, and package names simultaneously). "Relevance" is interpreted as returning results that match the query terms more closely, ranked by match quality.

3. **"Add filters" — no specification of which filters or filter types.**
   - Assumption: Add filtering by entity type (SBOM, advisory, package) and by severity (for advisories). These are the most obvious filterable dimensions based on the existing data model. Additional filters (date range, license type, etc.) can be added in follow-up work once requirements are clarified.

4. **"Should be fast enough" — no concrete performance NFR.**
   - Assumption: Ensure search queries complete within reasonable time by adding appropriate indexes and limiting result sets via pagination. No specific latency SLA is assumed.

5. **"Better UI" — marked as non-MVP, no frontend repository or design mockups available.**
   - **Excluded from scope.** Cannot be planned without design mockups or a frontend repository. This requirement should be addressed in a separate feature once designs are available.

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes for full-text search on searchable columns (SBOM name, advisory title/description, package name)
    - Extend SearchService to support ranked full-text search using PostgreSQL text search capabilities
    - Extend SearchService to support multi-entity search with entity-type and severity filtering
    - Add filter query parameters to the GET /api/v2/search endpoint (entity_type, severity)
    - Update search endpoint response to include relevance score and result type metadata
    - Add database migration for full-text search indexes
    - Update and expand search integration tests to cover filtering, ranking, and performance
```
