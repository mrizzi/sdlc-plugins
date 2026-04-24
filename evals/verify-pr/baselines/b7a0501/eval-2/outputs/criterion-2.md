## Criterion 2: Without threshold returns all severity counts (backward compatible)

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible).

**Result**: PASS

**Reasoning**:

The diff shows that when `params.threshold` is `None`, the code falls through to the `None => summary` branch, which returns the original unfiltered `AdvisorySummary` directly. This preserves the existing behavior -- all severity counts (critical, high, medium, low) are returned as they were before the change.

The `SummaryParams` struct uses `Option<String>` for the threshold field, so when the query parameter is omitted, it will be `None` by default, and Axum's `Query` extractor handles this correctly.

**Verdict**: PASS -- Backward compatibility is preserved when no threshold parameter is provided.
