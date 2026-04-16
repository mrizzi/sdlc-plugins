# Performance Optimization Task Template

This template extends the base `task-description-template.md` with performance-specific sections.

## Template

```
## Repository
<repository-name>

## Description
<What optimization this task achieves and why>

## Baseline Metrics

Current performance metrics before optimization (from baseline-report.md):

| Metric | Current (Baseline) | Unit |
|---|---|---|
| LCP (Largest Contentful Paint) | {{baseline-lcp}} | ms |
| FCP (First Contentful Paint) | {{baseline-fcp}} | ms |
| DOM Interactive (Time to Interactive) | {{baseline-domInteractive}} | ms |
| Total Load Time | {{baseline-total}} | ms |
| Bundle Size | {{baseline-bundle-size}} | KB |

## Target Metrics

Performance targets to achieve with this optimization:

| Metric | Target | Improvement | Unit |
|---|---|---|---|
| LCP (Largest Contentful Paint) | {{target-lcp}} | {{lcp-improvement}}% | ms |
| FCP (First Contentful Paint) | {{target-fcp}} | {{fcp-improvement}}% | ms |
| DOM Interactive (Time to Interactive) | {{target-domInteractive}} | {{domInteractive-improvement}}% | ms |
| Total Load Time | {{target-total}} | {{total-improvement}}% | ms |
| Bundle Size | {{target-bundle-size}} | {{bundle-improvement}}% | KB |

## Files to Modify
- `path/to/file.ext` — <brief reason>

## Files to Create
- `path/to/new_file.ext` — <purpose>

## API Changes
- `GET /v2/endpoint` — NEW: <description>
- `PUT /v2/endpoint/{id}` — MODIFY: <what changes in request/response>

## Implementation Notes
<Specific guidance: patterns to follow, existing code to reuse,
key functions/structs/components to interact with.
Reference actual file paths and symbol names found during repository analysis.>

## Reuse Candidates
- `path/to/file.ext::symbol_name` — <what it does and how it relates to this task>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Target metrics achieved (LCP ≤ {{target-lcp}}ms, FCP ≤ {{target-fcp}}ms)
- [ ] No performance regressions in non-target scenarios (< 5% degradation)

## Test Requirements
- [ ] Functional test description 1
- [ ] Functional test description 2

## Performance Test Requirements

- [ ] Re-run baseline capture for ALL scenarios (not just affected ones)
- [ ] Verify target scenario meets target metrics
- [ ] Verify non-target scenarios have no regressions (< 5% degradation in LCP, FCP, DOM Interactive, Total Load Time)
- [ ] Generate before/after comparison report
- [ ] If regression detected in non-target scenarios, prompt user for approval before committing

## Verification Commands
- `<command>` — <expected outcome>
- `node capture-baseline.mjs --config .claude/performance-config.md` — Should show improved metrics for target scenario

## Documentation Updates
- `path/to/doc.md` — <what content to add or revise>

## Dependencies
- Depends on: Task N — <task title> (if any)
```

## Rules

Follows all base template rules (from `shared/task-description-template.md`), plus:

- **Baseline Metrics** section is required — must reference actual baseline data
- **Target Metrics** section is required — targets must be realistic and measurable
- **Performance Test Requirements** section is required — defines regression testing criteria
- Omit non-applicable sections (API Changes, Files to Create, Documentation Updates, etc.) as per base template rules
- Target metrics should follow Google's Core Web Vitals "Good" thresholds unless application-specific requirements dictate otherwise:
  - LCP: ≤ 2.5s
  - FCP: ≤ 1.8s
  - DOM Interactive: ≤ 3.5s
- Improvement percentages help communicate expected impact clearly
