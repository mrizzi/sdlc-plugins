# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

## Analysis

The PR diff shows that when `params.threshold` is `None`, the code falls through to the `None => summary` branch, which returns the unfiltered `AdvisorySummary` directly. This preserves the existing behavior.

The `SummaryParams` struct uses `Option<String>` for the `threshold` field, meaning it is not required. When no `threshold` query parameter is provided, the struct will deserialize with `threshold: None`.

The `None` match arm simply returns the original `summary` object unchanged:

```rust
None => summary,
```

This preserves backward compatibility -- the endpoint returns all severity counts when no threshold is specified.

However, there is one issue related to criterion 5: the response does **not** include a `threshold_applied` boolean field. While this is a separate criterion, it means the response shape has changed (or should have changed) from the original. For the purposes of this criterion specifically (backward compatible severity counts), the `None` path does return all counts correctly.

**Conclusion:** The backward compatibility for returning all severity counts is maintained when no threshold parameter is provided. This criterion is **satisfied**.
