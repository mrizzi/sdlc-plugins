# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The acceptance criterion requires that the response JSON include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be `true` when a valid threshold parameter is provided and `false` (or absent) when no threshold is specified.

The PR diff does not add a `threshold_applied` field anywhere:

1. **No struct modification:** The `AdvisorySummary` struct is not modified in the diff. The struct is referenced but not defined in the changed files. No new field is added to it.

2. **No field in constructed response:** When constructing the filtered `AdvisorySummary` in the `Some(threshold)` arm, the code creates:
   ```rust
   AdvisorySummary {
       critical: summary.critical,
       high: if threshold_idx <= 1 { summary.high } else { 0 },
       medium: if threshold_idx <= 2 { summary.medium } else { 0 },
       low: if threshold_idx <= 3 { summary.low } else { 0 },
       total: summary.critical + summary.high + summary.medium + summary.low,
   }
   ```
   There is no `threshold_applied` field in this struct literal.

3. **No field in unfiltered response:** The `None` arm returns `summary` unmodified, which also lacks a `threshold_applied` field.

4. **The model file is not touched:** The `AdvisorySummary` struct is defined in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure, but this file does not appear in the diff at all.

This is a complete omission -- the feature was not implemented.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` in the constructed AdvisorySummary
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (should have been updated to add the field)
- The PR diff contains zero occurrences of `threshold_applied`
