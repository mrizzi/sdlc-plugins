---
name: performance-implement-optimization
description: |
  Execute performance optimization task by implementing code changes, running performance tests, comparing results against targets, and generating an isolated optimization result report.
argument-hint: "[jira-issue-id]"
---

# performance-implement-optimization skill

You are an AI performance optimization implementation assistant. You execute performance optimization tasks by reading structured Jira task descriptions (created by performance-plan-optimization), implementing code changes according to the optimization strategy, running performance tests, and updating Jira with results.

## Guardrails

- This skill modifies source code files in the target repository as specified in the Jira task
- This skill does NOT modify files outside the task scope
- This skill follows all constraints from implement-task (scope containment, code inspection before modification, conventional commits)
- This skill requires a Jira task created by performance-plan-optimization with performance-specific sections

**Apply:** [Execution Guardrails](../performance/execution-guardrails.template.md)

### Blocking Steps (this skill)
- Step 8 – Functional tests must pass before performance testing begins; halt if failing
- Step 9.0.5 – Baseline freshness decision (re-run baseline or proceed with stale)
- Step 9.4.R2 – Regression recovery decision (recover or abort PR)

### Completeness Requirements (this skill)
- All code changes from Jira task implemented before Step 8 (none deferred)
- All functional tests passing before Step 9 (no partial pass accepted)
- All configured scenarios measured in Step 9 (none skipped due to time)
- Complete optimization result report with all before/after metrics written before Step 13

### Error Handling (this skill)
- Functional test failures → halt at Step 8; do not proceed to performance testing
- Performance regression detected → halt at Step 9.4.R2 for user decision; do not
  auto-merge or auto-abort
- Step 4.5 Serena probe failure → do NOT halt; set `serena_mode = down`, continue
  with Read/Grep/Glob paths (Step 5-B)
- Jira MCP unavailable → trigger REST fallback; do not halt unless REST also fails

## Relationship to implement-task

This skill extends the `/sdlc-workflow:implement-task` workflow with performance-specific steps. The core implementation flow (Jira task parsing, code inspection, modification, commit, PR creation) follows implement-task exactly. The extensions are:

1. **Parse performance-specific sections** from Jira task (Baseline Metrics, Target Metrics, Performance Test Requirements)
2. **Performance testing phase** after implementation and functional tests
3. **Before/after comparison report** generation
4. **Performance results** posted to Jira task

## Step 1 – Validate Project Configuration

Before proceeding, read the project's CLAUDE.md and verify that the following sections exist under `# Project Configuration`:

1. `## Repository Registry` — must contain a table with at least one entry
2. `## Jira Configuration` — must contain at minimum: Project key, Cloud ID, Feature issue type ID
3. `## Code Intelligence` — must exist with the tool naming convention

If any of these sections are missing or incomplete, inform the user:

> "This skill requires Project Configuration in your CLAUDE.md. Please run `/setup` first to configure your project, then re-run this skill."

**Stop execution immediately.** Do not attempt to gather the missing information or proceed without it.

## Step 1.5 – JIRA Access Initialization

**Apply:** [Pattern 11: Jira Access Strategy](../performance/common-patterns.md#pattern-11-jira-access-strategy)

Before attempting any Jira operations (Steps 2, 3, 4, 11, 12), use the MCP-first approach with REST API fallback strategy defined in Pattern 11.

## Step 2 – Fetch and Parse Jira Task

Use Jira REST API to fetch the task:

```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  python3 "$plugin_root/scripts/jira-client.py" get_issue {task-id} --fields "*all"
```

Parse the structured description expecting these sections:

**Standard sections** (from implement-task):
- Repository
- Description
- Files to Modify
- Files to Create
- Implementation Notes
- Acceptance Criteria
- Test Requirements
- Dependencies

**Performance-specific sections** (extension):
- **Baseline Metrics** — Current performance metrics before optimization
- **Target Metrics** — Expected metrics after optimization
- **Performance Test Requirements** — How to verify performance improvement

Extract and store all sections for use in later steps.

## Step 3 – Verify Dependencies

If the task has Dependencies, check each one:

jira.get_issue(<dependency-id>)

Verify status is Done or equivalent. If not, stop and inform the user.

## Step 4 – Transition to In Progress and Assign

Transition the Jira issue to indicate work has started, and assign it to the current user:

1. Retrieve the current user's Jira account ID:

jira.user_info()

2. Assign the task to the current user:

jira.edit_issue(<jira-issue-id>, assignee=<current-user-account-id>)

3. Transition the issue to In Progress:

jira.transition_issue → In Progress

This ensures both ownership and status are reflected in Jira as soon as implementation begins.

## Step 4.5 – Serena Availability Probe

Read `serena_instance` from the **target repository's** `CLAUDE.md`:

```bash
serena_instance=$(grep -A5 "Repository Registry" CLAUDE.md \
  | grep -v "^|---|" | grep "^|" \
  | awk -F'|' 'NR==2{print $4}' | xargs)
```

**If `serena_instance` is non-empty and not "—":**

Call `mcp__{serena_instance}__get_symbols_overview` with `relative_path="."`.

- **Response received (any result):** `serena_mode = live`. Store the overview. Proceed to **Step 5-A**.
- **Error response:** `serena_mode = down`. Record exact error string. Proceed to **Step 5-B**.

**If `serena_instance` is "—" or empty:** `serena_mode = not-configured`. Proceed to **Step 5-B**.

> `serena_mode` is set once here and applies for the duration of Step 5 code inspection.

---

## Step 5 – Understand the Code

**Apply:** [Common Pattern: Code Intelligence Strategy — Pattern 8](../performance/common-patterns.md#pattern-8-code-intelligence-strategy-serena-first-with-grep-fallback)

(`serena_mode` was set in Step 4.5.)

---

### Step 5-A – Code Inspection via Serena (`serena_mode = live`)

> Read and Grep are not available for symbol discovery in this path.

Using `mcp__{serena_instance}__<tool>` for all code inspection:

1. **Overview without full reads:** `get_symbols_overview` on files to modify to see
   their structure (classes, functions, types) without reading the entire file.
2. **Read only what you need:** `find_symbol` with `include_body=true` to read the
   specific functions, structs, or components you need to understand or change.
3. **Check backward compatibility:** `find_referencing_symbols` on any symbol you plan
   to modify to identify all callers and ensure your changes won't break them.
4. **Non-symbolic search:** `search_for_pattern` for configuration, string literals,
   or patterns not captured as symbols.
5. **Convention conformance:** `get_symbols_overview` on 2–3 sibling files to understand
   their structure and patterns.

> Check the **Code Intelligence** section of the project's CLAUDE.md for per-instance
> limitations. Adapt tool usage accordingly.

---

### Step 5-B – Code Inspection via Read/Grep/Glob (`serena_mode = down | not-configured`)

> Entered when Step 4.5 probe recorded `serena_mode = down` or `not-configured`.

Use Read, Grep, and Glob tools for all code inspection:

1. Read files to modify in full or in targeted sections
2. Grep for patterns, string literals, and configuration
3. Glob to discover sibling files and module structure

---

Goals (both paths):
- understand the current state of files to be modified
- confirm the patterns referenced in Implementation Notes exist
- identify any conflicts with recent changes
- search for existing utilities, helpers, and shared modules that provide functionality overlapping with the planned changes — if equivalent logic already exists, plan to reuse or extend it rather than writing new code
- identify established conventions from sibling code for use during implementation

## Step 6 – Create Branch

Create a feature branch named after the Jira issue:

```bash
git checkout -b {jira-issue-id}
```

**Note:** Performance optimization tasks do not use the Target PR flow (review feedback fixes are not applicable to performance optimizations), so always create a new branch.

## Step 7 – Implement Optimization

Implement the optimization described in the task's Description section. Use Files to Modify and Files to Create as the working scope. Follow Implementation Notes for patterns and code references.

**Performance optimization types** (examples):

- **Bundle size reduction:** Code splitting, lazy loading, tree shaking, dead code elimination
- **API optimization:** Reduce over-fetching, eliminate N+1 queries, parallel fetching
- **Render optimization:** Component memoization, virtual scrolling, avoid layout thrashing
- **Resource optimization:** Async/defer scripts, parallel loading, image compression
- **Long task mitigation:** Code splitting, web workers, async patterns
- **Service chain optimization:** Eliminate hidden N+1 queries at service/model layer (detected via call graph), add missing database indexes
- **Wasted computation elimination:** Create targeted service methods or projections so handlers fetch only the data they use

Follow the same code modification principles as implement-task:
- Reuse existing code when possible
- Follow conventions discovered during code inspection
- Keep changes scoped to the task
- Do not introduce unrelated refactoring

## Step 8 – Run Functional Tests

Try `npm test`. If tests fail, fix and re-run. If no tests configured, prompt:

> Does this project have tests? (1) Yes - provide test command (2) No - skip to manual verification

Execute provided test command or proceed with user confirmation for manual testing.

## Step 9 – Performance Testing Phase

**This is the key extension to implement-task.**

### Step 9.0.5 – Check Baseline Freshness

Read `metadata.baseline_commit_sha` from config. If workflow files changed since baseline commit, prompt: (1) Continue with existing baseline (2) Re-baseline first (3) Cancel. If option 2, instruct user to run `/sdlc-workflow:performance-baseline` first.

### Step 9.1 – Capture Current Performance Metrics

Re-run the performance baseline capture for scenarios affected by this optimization.

**Determine affected scenarios and metric type:**
- Read `.claude/performance-config.md` from the target repository
- **Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-6-workflow-validation)
- Read `metadata.metric_type` to determine capture method
- Filter scenarios to those in the selected workflow

**Read baseline capture mode from config metadata (Updated):**

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction) and [Common Pattern: Mode Consistency Enforcement](../performance/common-patterns.md#pattern-3-mode-consistency-enforcement)

**Specific fields to extract:**
- `metadata.baseline_mode` → baseline_mode (use same mode as original baseline)
- `metadata.metric_type` → metric_type (frontend | backend | hybrid)

**Use stored mode automatically** (no user prompt):

> ℹ️ Using baseline capture mode: **{baseline_mode}** (from original baseline)
> ℹ️ Metric type: **{metric_type}**

**Note:** Mode consistency is enforced to ensure valid performance comparisons. The mode was set during the original baseline capture and is read from config metadata.

**Execute baseline capture based on metric_type:**

**If metric_type = "frontend" or "hybrid" (Playwright capture):**

1. Locate the plugin cache and copy the capture script to the baseline directory:
   ```bash
   # Resolve plugin root (Pattern 0: Plugin Root Resolution)
   plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null \
     | sort -V | tail -1)
   
   if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then
     echo "❌ sdlc-workflow plugin not found in ~/.claude/plugins/cache/"
     echo "   Ensure the plugin is installed and try again."
     exit 1
   fi
   
   template_path="${plugin_root}skills/performance/capture-baseline.template.mjs"
   
   if [ ! -f "$template_path" ]; then
     echo "❌ Capture script template not found at: $template_path"
     echo "   Plugin may be corrupted. Please reinstall the sdlc-workflow plugin."
     exit 1
   fi
   
   cp "$template_path" "{baseline-directory}/capture-baseline-current.mjs"
   chmod +x "{baseline-directory}/capture-baseline-current.mjs"
   ```
   
   **Note:** Uses `{baseline-directory}` instead of `/tmp` for consistency with baseline skill and to preserve the script used for each optimization run (audit trail).

2. Extract the application port from configuration:
   ```bash
   # Read port stored by performance-baseline (Step 7.4) in Development Environment section
   port=$(grep "| Port |" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
   
   if [ -z "$port" ] || [ "$port" = "TBD" ]; then
     echo "❌ Application port not configured."
     echo "Please run /sdlc-workflow:performance-baseline first so the port is discovered and stored."
     exit 1
   fi
   ```

3. Run the capture script:
   ```bash
   node "{baseline-directory}/capture-baseline-current.mjs" \
     --config "{path-to-performance-config.md}" \
     --port "$port" \
     --mode cold-start
   ```

4. Parse the JSON output to extract current frontend metrics (LCP, FCP, DOM Interactive, Total Load Time, bundle size)

**If metric_type = "backend" or "hybrid" (curl/bc benchmarking):**

**Apply:** [Pattern 10: API Profiling](../performance/common-patterns.md#pattern-10-api-profiling)

**Use baseline configuration:**
- Port: from Performance Scenarios table
- Iterations: from Baseline Settings table
- Endpoints: from Selected Workflow scenarios

**Store metrics:** p50, p95, p99 (milliseconds) for each endpoint

**Compare metrics:** Before (original baseline) vs After (current) using same mode for accurate comparison.

### Step 9.2 – Compare Against Baseline and Targets

Read `metadata.metric_type` from configuration to determine which metrics to compare.

Read the Baseline Metrics and Target Metrics from the Jira task description (parsed in Step 2).

**If metric_type = "frontend" or "hybrid":**

For each frontend metric (LCP, FCP, DOM Interactive, bundle size):
- **Baseline:** Starting value before optimization
- **Current:** Measured value after optimization
- **Target:** Goal value from task
- **Improvement:** `baseline - current`
- **Progress to target:** `(improvement / (baseline - target)) * 100`

**If metric_type = "backend" or "hybrid":**

For each backend metric (Response Time p95/p99, Throughput, Error Rate):
- **Baseline:** Starting value before optimization
- **Current:** Measured value after optimization
- **Target:** Goal value from task
- **Improvement:** 
  - For latency metrics: `baseline - current` (lower is better)
  - For throughput: `current - baseline` (higher is better)
  - For error rate: `baseline - current` (lower is better)
- **Progress to target:** `(improvement / (baseline - target)) * 100`

### Step 9.3 – Generate Before/After Comparison Report

Create a comparison table showing the results based on metric_type:

**If metric_type = "frontend" or "hybrid":**

```markdown
## Frontend Performance Test Results

| Metric | Baseline | Current | Target | Improvement | Progress to Target |
|---|---|---|---|---|---|
| LCP (p95) | {baseline-lcp} ms | {current-lcp} ms | {target-lcp} ms | {improvement-lcp} ms ({percentage}%) | {progress}% |
| FCP (p95) | {baseline-fcp} ms | {current-fcp} ms | {target-fcp} ms | {improvement-fcp} ms ({percentage}%) | {progress}% |
| DOM Interactive (p95) | {baseline-domInteractive} ms | {current-domInteractive} ms | {target-domInteractive} ms | {improvement-domInteractive} ms ({percentage}%) | {progress}% |
| Bundle Size | {baseline-size} KB | {current-size} KB | {target-size} KB | {improvement-size} KB ({percentage}%) | {progress}% |
```

**If metric_type = "backend" or "hybrid":**

```markdown
## Backend Performance Test Results

| Metric | Baseline | Current | Target | Improvement | Progress to Target |
|---|---|---|---|---|---|
| Response Time (p95) | {baseline-resp-p95} ms | {current-resp-p95} ms | {target-resp-p95} ms | {improvement-resp-p95} ms ({percentage}%) | {progress}% |
| Response Time (p99) | {baseline-resp-p99} ms | {current-resp-p99} ms | {target-resp-p99} ms | {improvement-resp-p99} ms ({percentage}%) | {progress}% |
| Throughput | {baseline-throughput} req/sec | {current-throughput} req/sec | {target-throughput} req/sec | {improvement-throughput} req/sec ({percentage}%) | {progress}% |
| Error Rate | {baseline-error} % | {current-error} % | {target-error} % | {improvement-error} % ({percentage}%) | {progress}% |
```

**Status (for all metric types):**
- ✅ Target met: {metrics-that-met-target}
- ⚠️ Improved but target not met: {metrics-improved-but-not-at-target}
- ❌ Regressed: {metrics-that-regressed}

### Step 9.4 – Verify Target Metrics

**Step 9.4.0 – Apply Measurement Noise Tolerance**

Performance measurements have inherent variance. A metric regression is only flagged if BOTH conditions are met.

**Frontend Metrics Regression Thresholds (if metric_type = "frontend" or "hybrid"):**

1. **Relative threshold:** Metric worsens by more than **5%**
2. **Absolute threshold:** 
   - Time metrics (LCP, FCP, DOM Interactive, Total Load Time): worsen by more than **50ms**
   - Size metrics (bundle size, transfer size): worsen by more than **10KB**

**Frontend Example:**
- Baseline LCP: 2000ms, Current LCP: 2030ms
  - Delta: +30ms (+1.5%)
  - Result: **PASS** (within noise tolerance, < 50ms absolute AND < 5% relative)
  
- Baseline LCP: 2000ms, Current LCP: 2150ms
  - Delta: +150ms (+7.5%)
  - Result: **FAIL** (exceeds both thresholds)

**Backend Metrics Regression Thresholds (if metric_type = "backend" or "hybrid"):**

1. **Response time metrics (p95, p99):**
   - Relative threshold: > **10%** increase
   - Absolute threshold: > **50ms** increase
   - Both conditions must be met to flag regression

2. **Throughput:**
   - Relative threshold: > **20%** decrease
   - No absolute threshold (depends on baseline capacity)

3. **Error rate:**
   - Absolute threshold: > **1%** increase (e.g., 0.1% → 1.2%)
   - Critical if error rate > 5% (any value)

**Backend Example:**
- Baseline Response Time p95: 200ms, Current: 220ms
  - Delta: +20ms (+10%)
  - Result: **PASS** (10% relative but only 20ms absolute, < 50ms)
  
- Baseline Response Time p95: 200ms, Current: 280ms
  - Delta: +80ms (+40%)
  - Result: **FAIL** (exceeds both 50ms and 10% thresholds)

- Baseline Throughput: 100 req/sec, Current: 75 req/sec
  - Delta: -25 req/sec (-25%)
  - Result: **FAIL** (exceeds 20% decrease threshold)

Differences within these bands are measurement noise and should not block the PR.

**Step 9.4.1 – Check Target Achievement**

Check if all target metrics were achieved:

- **All targets met:** Proceed to Step 9.5 (create result report)
- **Some targets not met but improvement achieved:** Proceed to Step 9.5, but flag in Jira comment
- **Any metric regressed beyond noise tolerance:** Execute the recovery procedure below before stopping.

#### Regression Recovery Procedure

If any metric is worse than the baseline value **beyond noise tolerance** (see Step 9.4.0), perform these steps in order:

#### Regression Recovery Steps

**Step 9.4.R1 – Save regression context**

Write a regression report to preserve diagnostic information:

```bash
timestamp=$(date -u +"%Y-%m-%dT%H-%M-%S")
regression_file=".claude/performance/optimization-results/${jira_key}-regression-${timestamp}.md"
mkdir -p .claude/performance/optimization-results
```

Write the file with:
```markdown
# Regression Report: {jira-key}

**Detected:** {iso-timestamp}
**Branch:** {git-branch}

## Regressed Metrics

| Metric | Baseline | After Change | Delta |
|---|---|---|---|
| {metric-name} | {baseline-value} | {current-value} | {delta} |

## Implementation Context

Files modified during this task (from `git status`):
{git status output}

## Recovery Instructions

1. Review the code changes that caused the regression
2. Fix the regression and re-run `/sdlc-workflow:performance-implement-optimization {jira-key}`
3. Or discard changes: `git stash drop` (after reviewing with `git stash show -p`)

Regression report saved for audit trail.
```

**Step 9.4.R2 – Prompt user for action**

Present the regression details and offer two options:

> ❌ **Performance regression detected**
>
> {metric-name}: Baseline {baseline-value} → Current {current-value} ({delta})
>
> Regression report saved to: `.claude/performance/optimization-results/{jira_key}-regression-{timestamp}.md`
>
> **Choose how to proceed:**
> 1. **Stash changes** — Preserve code for review, stop execution (recommended)
> 2. **Proceed with warning** — Continue despite regression
>
> Choose (1/2):

**If "1. Stash changes":**

**Only stash uncommitted working tree changes** — do NOT run `git reset`. At this point in the
workflow (Step 9, before Step 10 commits), no commit has been made yet. The stash preserves all
modified files so the developer can inspect them with `git stash show -p` or recover them with
`git stash pop`.

```bash
git stash push -m "perf-regression-stash: {jira-key} at {timestamp}"
```

Inform user:

> Changes stashed. To inspect or restore:
> - View changes: `git stash show -p`
> - Restore to investigate: `git stash pop`
> - Discard entirely: `git stash drop`
>
> Fix the regression and re-run `/sdlc-workflow:performance-implement-optimization {jira-key}` to try again.

Stop execution.

**If "2. Proceed with warning":**

> ⚠️ **Proceeding with known performance regression**
>
> {metric-name} regressed by {delta}. The optimization result report will record
> `status: regression_acknowledged`. A human reviewer must explicitly approve the PR.
>
> Document the reason for accepting this regression in the PR description before merging.

Continue to Step 9.5, passing `status: regression_acknowledged` to the result report instead of `pending_verification`.

### Step 9.5 – Create Optimization Result Report

After capturing current performance metrics and validating no regressions, create an optimization result report for audit trail and verification:
b
**Step 9.5.1 – Generate Report Filename**

Create timestamped report filename:

```bash
timestamp=$(date -u +"%Y-%m-%dT%H-%M-%S")
report_file=".claude/performance/optimization-results/${jira_key}-${timestamp}.md"
```

Ensure directory exists:

```bash
mkdir -p .claude/performance/optimization-results
```

**Step 9.5.2 – Prepare Report Data**

Extract required data for the report:

- **Jira key:** From task (e.g., TC-5002)
- **Workflow name:** From config metadata
- **Timestamp:** ISO 8601 format
- **Branch:** Current git branch (`git branch --show-current`)
- **Commit SHA:** Current commit (`git rev-parse HEAD`)
- **Baseline commit SHA:** From config metadata.baseline_commit_sha
- **Capture mode:** From config metadata.baseline_mode
- **Task summary:** From Jira task
- **Baseline metrics:** From config Optimization Targets table (Baseline column)
- **Current metrics:** From Step 9.1 capture results (p95 values)
- **Target metrics:** From config Optimization Targets table (Target column)
- **Delta calculations:** baseline - current for each metric
- **Status per metric:** "Met ✓" if current ≤ target, "Partial" if improved but > target, "Regression ✗" if worse
- **Scenarios measured:** List from config Performance Scenarios
- **Files changed:** From git status/diff
- **Validation checks:** List from Step 9.4 (no regressions, baseline freshness)

**Step 9.5.3 – Generate Report from Template**

Use the optimization-result template:

```markdown
---
metadata:
  jira_key: {jira-key}
  workflow: {workflow-name}
  timestamp: {iso-timestamp}
  branch: {git-branch}
  commit_sha: {commit-sha}
  baseline_commit_sha: {baseline-commit-sha}
  capture_mode: {capture-mode}
  status: pending_verification
---

# Optimization Result: {jira-key}

**Task:** {task-summary}  
**Workflow:** {workflow-name}  
**Executed:** {formatted-timestamp}  
**Branch:** {git-branch}

## Performance Impact

**If metric_type = "frontend" or "hybrid", include:**

### Frontend Metrics

| Metric | Baseline (p95) | After Optimization (p95) | Delta | Target | Status |
|---|---|---|---|---|---|
| LCP | {baseline-lcp}ms | {current-lcp}ms | {delta-lcp} | {target-lcp}ms | {status-lcp} |
| FCP | {baseline-fcp}ms | {current-fcp}ms | {delta-fcp} | {target-fcp}ms | {status-fcp} |
| DOM Interactive | {baseline-dom}ms | {current-dom}ms | {delta-dom} | {target-dom}ms | {status-dom} |
| Total Load Time | {baseline-total}ms | {current-total}ms | {delta-total} | {target-total}ms | {status-total} |

**If metric_type = "backend" or "hybrid", include:**

### Backend Metrics

| Metric | Baseline (p95) | After Optimization (p95) | Delta | Target | Status |
|---|---|---|---|---|---|
| Response Time (p95) | {baseline-resp-p95}ms | {current-resp-p95}ms | {delta-resp-p95} | {target-resp-p95}ms | {status-resp-p95} |
| Response Time (p99) | {baseline-resp-p99}ms | {current-resp-p99}ms | {delta-resp-p99} | {target-resp-p99}ms | {status-resp-p99} |
| Throughput | {baseline-throughput} req/sec | {current-throughput} req/sec | {delta-throughput} | {target-throughput} req/sec | {status-throughput} |
| Error Rate | {baseline-error}% | {current-error}% | {delta-error} | {target-error}% | {status-error} |

**Performance Summary:**
- {summary-line: e.g., "Response Time (p95) improved by 50ms (25%), 75% to target"}
- {summary-line: e.g., "Throughput increased by 20 req/sec (20%), 50% to target"}

## Test Scenarios Measured

{scenarios-list: one bullet per scenario with p95 result}

## Code Changes

- Commit: {commit-sha}
- PR: (will be added after PR creation)
- Files modified: {files-changed}

## Validation

{validation-checks: bullet list of checks performed}

## Next Steps

- Verify PR passes acceptance criteria with `/sdlc-workflow:performance-verify-optimization {jira-key}`
- After PR merge to main, re-run `/sdlc-workflow:performance-baseline` to update configuration with fresh metrics
- Continue with remaining optimization tasks if targets not fully met
```

**Step 9.5.4 – Write Report File**

Write the report to the generated filename:

```bash
cat > "${report_file}" <<'EOF'
{report-content}
EOF
```

**Step 9.5.5 – Log Report Creation**

Log to user:

```
✓ Optimization result report created:
  - File: {report_file}
  - Status: pending_verification
  - Performance impact:
    • LCP (p95): {baseline} → {current} ({delta})
    • FCP (p95): {baseline} → {current} ({delta})
    • DOM Interactive (p95): {baseline} → {current} ({delta})
    • Total Load Time (p95): {baseline} → {current} ({delta})

```

**Note:** This approach eliminates race conditions by writing to isolated per-task report files instead of shared config. The configuration's "Latest Verified" column is updated by `/sdlc-workflow:performance-verify-optimization` after verification passes.

## Step 10 – Commit Changes

Create a commit using Conventional Commits format:

```bash
git commit -m "$(cat <<'EOF'
perf({scope}): {brief-description}

{detailed-description}

Performance impact:
- {metric-1}: {improvement-1}
- {metric-2}: {improvement-2}

Jira-Issue-Id: {jira-issue-id}

Assisted-by: Claude <noreply@anthropic.com>
EOF
)"
```

**Commit type:** Use `perf` for performance optimizations (Conventional Commits spec).

**Include performance impact:** Add a "Performance impact:" section in the commit body showing the measured improvements.

## Step 11 – Push Branch and Open PR

Push the branch:

```bash
git push -u origin {jira-issue-id}
```

Create a pull request:

```bash
gh pr create \
  --title "{task-summary}" \
  --body "$(cat <<'EOF'
## Summary

{task-description}

## Performance Impact

{before-after-comparison-table}

## Changes

{list-of-files-modified}

## Testing

- [x] Functional tests pass (or manual verification completed)
- [x] Performance baseline re-captured
- [x] Metrics compared against targets

Related Jira: {jira-url}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Extract the PR URL from the output.

## Step 12 – Update Jira with Performance Results

Look up the **Git Pull Request custom field** ID from the project's **Jira Configuration**
section in CLAUDE.md (the field is listed as `Git Pull Request custom field: <field-id>`).

- **If configured**, update that custom field on the Jira issue with the PR URL.
  The field requires ADF (Atlassian Document Format), not a plain string:

jira.update_issue(<jira-issue-id>, fields={"<field-id>": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})

- **If not configured**, skip the custom field update — the PR link will still be included in the Jira comment below.

Add a comment to the Jira task:

jira.add_comment

Include:
- PR link
- Performance test results (before/after comparison table)
- Status of target achievement
- Summary of changes made

**Comment format:**

```markdown
## Performance Optimization Complete

**PR:** {pr-url}

{before-after-comparison-table-from-step-9.3}

**Summary:**
- {count} of {total} target metrics achieved
- Overall improvement: {summary-of-improvements}

**Next Steps:**
- Review the PR and verify functional correctness
- Run `/sdlc-workflow:performance-verify-optimization {task-id}` to validate optimization in CI
- Merge the PR once approved

---

This comment was AI-generated by [sdlc-workflow/performance-implement-optimization](https://github.com/mrizzi/sdlc-plugins) v{version}.
```

Transition the task:

```bash
# Get available transitions for the task
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  python3 "$plugin_root/scripts/jira-client.py" get_transitions {task-id}

# Parse output to find "In Review" transition ID
# Example output: [{"id": "51", "name": "In Review"}, {"id": "31", "name": "Done"}]
# Extract the ID where name matches "In Review"

# Transition using discovered ID
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  python3 "$plugin_root/scripts/jira-client.py" transition_issue {task-id} \
    --transition-id {discovered-in-review-id}
```

**Note:** Transition IDs vary by Jira project workflow configuration. Always discover transitions dynamically rather than hardcoding IDs.

## Step 13 – Output Summary

Report to the user:

> ✅ **Performance optimization implemented successfully!**
>
> **Task:** {task-id} — {task-summary}  
> **PR:** {pr-url}
>
> **Performance Results:**
> {summary-table}
>
> **Status:**
> - ✅ {count} of {total} target metrics achieved
> - Overall improvement: {summary}
>
> **Next Steps:**
> 1. Review the PR for functional correctness
> 2. Run `/sdlc-workflow:performance-verify-optimization {task-id}` in CI
> 3. Merge the PR once approved

If some targets were not met:

> ⚠️ **Note:** Not all target metrics were achieved, but measurable improvement was observed. Consider:
> - Running additional optimization iterations
> - Adjusting targets if they were too aggressive
> - Investigating if external factors affected measurements

## Important Rules

- Follow all constraints from implement-task (scope containment, code inspection, conventional commits)
- Always attempt functional tests before performance tests
- If no automated tests exist, require manual regression verification before proceeding
- Do not proceed if any metric regresses — stop and inform user
- Performance metrics should be captured using the same conditions as the baseline (test data loaded, app running)
- Commit message MUST include "Performance impact:" section with measured improvements
- PR body MUST include before/after comparison table
- Jira comment MUST include full performance test results
- If baseline capture fails (app not running, Playwright not installed), stop and inform user with actionable remediation
- Do not modify source code files outside the task scope
- Do not implement optimizations not described in the task
- Do not skip functional tests or manual verification to save time
- Do not fabricate performance metrics — always run actual baseline capture
