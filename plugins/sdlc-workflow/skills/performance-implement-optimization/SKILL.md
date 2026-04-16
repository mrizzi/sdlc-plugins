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

## Relationship to implement-task

This skill extends the `/sdlc-workflow:implement-task` workflow with performance-specific steps. The core implementation flow (Jira task parsing, code inspection, modification, commit, PR creation) follows implement-task exactly. The extensions are:

1. **Parse performance-specific sections** from Jira task (Baseline Metrics, Target Metrics, Performance Test Requirements)
2. **Performance testing phase** after implementation and functional tests
3. **Before/after comparison report** generation
4. **Performance results** posted to Jira task

## Step 1 – Validate Project Configuration

(Same as implement-task Step 0)

Read the project's CLAUDE.md and verify that the following sections exist under `# Project Configuration`:
- Repository Registry
- Jira Configuration
- Code Intelligence

If missing, inform the user and stop execution.

## Step 2 – Fetch and Parse Jira Task

(Same as implement-task Step 1, with extensions)

Use Jira REST API to fetch the task:

```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py get_issue {task-id} --fields "*all"
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

(Same as implement-task Step 2)

If the task has Dependencies, verify each dependency is Done. If not, stop and inform the user.

## Step 4 – Transition to In Progress and Assign

(Same as implement-task Step 3)

Assign the task to the current user and transition to In Progress.

## Step 5 – Understand the Code

(Same as implement-task Step 4)

Inspect the files listed in Files to Modify using Serena (if available) or Read/Grep/Glob tools.

Goals:
- Understand current state of files to be modified
- Confirm patterns referenced in Implementation Notes exist
- Identify any conflicts with recent changes
- Discover established conventions from sibling code

## Step 6 – Create Branch

(Same as implement-task Step 5)

Create a feature branch named after the Jira issue:

```bash
git checkout -b {jira-issue-id}
```

## Step 7 – Implement Optimization

(Same as implement-task Step 6, with performance context)

Implement the optimization described in the task's Description section. Use Files to Modify and Files to Create as the working scope. Follow Implementation Notes for patterns and code references.

**Performance optimization types** (examples):

- **Bundle size reduction:** Code splitting, lazy loading, tree shaking, dead code elimination
- **API optimization:** Reduce over-fetching, eliminate N+1 queries, parallel fetching
- **Render optimization:** Component memoization, virtual scrolling, avoid layout thrashing
- **Resource optimization:** Async/defer scripts, parallel loading, image compression
- **Long task mitigation:** Code splitting, web workers, async patterns

Follow the same code modification principles as implement-task:
- Reuse existing code when possible
- Follow conventions discovered during code inspection
- Keep changes scoped to the task
- Do not introduce unrelated refactoring

## Step 8 – Run Functional Tests

### Step 8.1 – Attempt Standard Test Command

Try to run the project's test suite with the standard npm command:

```bash
npm test
```

### Step 8.2 – Handle Test Execution Outcomes

**If tests pass:**
- Proceed to Step 9 (Performance Testing Phase)

**If tests fail with actual test failures:**
- Diagnose the failure
- Fix the issue in the implementation
- Re-run tests until they pass
- Then proceed to Step 9

**If `npm test` command fails or no tests are configured:**
- Check the error message:
  - "Missing script: test" or similar → no test script configured
  - "Error: no test specified" → test script exists but is a placeholder
  - Other errors → legitimate test failures, handle as above

### Step 8.3 – Prompt User for Test Configuration

If no tests are configured or available, prompt the user:

> **No automated tests found.**
>
> Does this project have a test suite?
>
> Options:
> 1. Yes - I'll provide the test script path and execution instructions
> 2. No - Skip automated tests and recommend manual regression verification
>
> Choose (1/2):

**If user chooses "1. Yes":**

Prompt for test details:

> Please provide the test script details:
>
> 1. **Test script path** (e.g., `scripts/test.sh`, `package.json` script name)
> 2. **Execution command** (e.g., `npm run test:unit`, `./scripts/test.sh`)
> 3. **Expected success indicator** (e.g., "All tests passed", exit code 0)

Execute the provided command:

```bash
{user-provided-test-command}
```

Handle results as in Step 8.2 (pass → proceed, fail → diagnose and fix).

**If user chooses "2. No":**

Inform the user to perform manual regression verification:

> ⚠️ **Manual regression verification required**
>
> No automated tests are available for this project. Please manually verify that:
> - The application still functions correctly after the optimization
> - No regressions were introduced in the modified code paths
> - The optimization did not break any existing functionality
>
> **Recommended verification steps:**
> 1. Start the application locally
> 2. Navigate through the optimized workflow
> 3. Verify all features work as expected
> 4. Check browser console for errors
>
> Once manual verification is complete, the skill will proceed with performance testing.
>
> **Ready to proceed?** (yes/no)

**If user responds "yes":**
- Proceed to Step 9 (Performance Testing Phase)

**If user responds "no":**
- Stop execution and inform user:
  > "Optimization implementation paused. Complete manual verification and re-run this skill to continue."

## Step 9 – Performance Testing Phase

**This is the key extension to implement-task.**

### Step 9.0.5 – Check Baseline Freshness (New)

Before capturing current performance metrics, validate that the original baseline is not stale:

**Read baseline commit SHA from config metadata:**

```bash
# Read performance-config.md
if config has metadata.baseline_commit_sha:
  baseline_commit_sha = metadata.baseline_commit_sha
  
  if baseline_commit_sha == "unknown":
    log info:
    > ℹ️ **Baseline was captured without git tracking**
    >
    > Baseline commit SHA: unknown
    > Skipping freshness check (baseline was captured in a non-git directory)
    
    skip to Step 9.1
else:
  # v1 config or baseline not yet captured
  skip freshness check, proceed to Step 9.1
```

**Compare baseline commit with current branch:**

```bash
# Get current branch's base commit (where it diverged from main)
current_base_commit=$(git merge-base HEAD main)

# Count commits since baseline
commit_count=$(git rev-list --count ${baseline_commit_sha}..HEAD)

# Get list of workflow files changed since baseline
changed_files=$(git diff --name-only ${baseline_commit_sha}..HEAD | grep -E "(src/|client/|pages/)")
```

**If commits since baseline affect workflow files:**

Inform the user:

> ⚠️ **Baseline may be stale**
>
> The original baseline was captured at commit: `{baseline_commit_sha}`
>
> Since then, **{commit_count}** commits have been made, including changes to workflow files:
> - `{changed_file_1}`
> - `{changed_file_2}`
> - ... (up to 10 files)
>
> Stale baselines can produce misleading comparisons if the workflow structure changed.
>
> **Options:**
> 1. **Continue** with existing baseline (valid if changes don't affect measured workflow)
> 2. **Re-baseline** before optimization (recommended if workflow changed significantly)
> 3. **Cancel** and investigate changes
>
> Choose (1/2/3):

**If user selects option 1:** Continue to Step 9.1

**If user selects option 2:** 
- Inform user: "Please run `/sdlc-workflow:performance-baseline` first to refresh the baseline, then re-run this task."
- Stop execution

**If user selects option 3:** Stop execution

**If no workflow files changed or commit count < 5:**
- Skip warning, proceed to Step 9.1

### Step 9.1 – Capture Current Performance Metrics

Re-run the performance baseline capture for scenarios affected by this optimization.

**Determine affected scenarios:**
- Read `.claude/performance-config.md` from the target repository
- **Apply:** [Common Pattern: Workflow Validation](../performance/common-patterns.md#pattern-7-workflow-validation)
- Filter scenarios to those in the selected workflow

**Read baseline capture mode from config metadata (Updated):**

**Apply:** [Common Pattern: Metadata Extraction](../performance/common-patterns.md#pattern-2-metadata-extraction) and [Common Pattern: Mode Consistency Enforcement](../performance/common-patterns.md#pattern-3-mode-consistency-enforcement)

**Specific field to extract:**
- `metadata.baseline_mode` → baseline_mode (use same mode as original baseline)

**Use stored mode automatically** (no user prompt):

> ℹ️ Using baseline capture mode: **{baseline_mode}** (from original baseline)

**Note:** Mode consistency is enforced to ensure valid performance comparisons. The mode was set during the original baseline capture and is read from config metadata.

**Execute baseline capture:**

1. Locate the plugin cache and copy the capture script to the baseline directory:
   ```bash
   # Resolve plugin cache path (same as performance-baseline Step 8.1)
   plugin_cache="${HOME}/.claude/plugins/cache/sdlc-plugins-local/sdlc-workflow"
   plugin_version=$(ls "$plugin_cache" | sort -V | tail -n 1)
   template_path="${plugin_cache}/${plugin_version}/skills/performance/capture-baseline.template.mjs"
   
   if [ ! -f "$template_path" ]; then
     echo "❌ Capture script template not found at: $template_path"
     echo "Plugin may be corrupted or not installed. Please reinstall the sdlc-workflow plugin."
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

4. Parse the JSON output to extract current metrics (LCP, FCP, DOM Interactive, Total Load Time, bundle size)

**Compare metrics:** Before (original baseline) vs After (new baseline) using same mode for accurate comparison.

### Step 9.2 – Compare Against Baseline and Targets

Read the Baseline Metrics and Target Metrics from the Jira task description (parsed in Step 2).

For each metric (LCP, FCP, DOM Interactive, bundle size):
- **Baseline:** Starting value before optimization
- **Current:** Measured value after optimization
- **Target:** Goal value from task
- **Improvement:** `baseline - current`
- **Progress to target:** `(improvement / (baseline - target)) * 100`

### Step 9.3 – Generate Before/After Comparison Report

Create a comparison table showing the results:

```markdown
## Performance Test Results

| Metric | Baseline | Current | Target | Improvement | Progress to Target |
|---|---|---|---|---|---|
| LCP (p95) | {baseline-lcp} ms | {current-lcp} ms | {target-lcp} ms | {improvement-lcp} ms ({percentage}%) | {progress}% |
| FCP (p95) | {baseline-fcp} ms | {current-fcp} ms | {target-fcp} ms | {improvement-fcp} ms ({percentage}%) | {progress}% |
| DOM Interactive (p95) | {baseline-domInteractive} ms | {current-domInteractive} ms | {target-domInteractive} ms | {improvement-domInteractive} ms ({percentage}%) | {progress}% |
| Bundle Size | {baseline-size} KB | {current-size} KB | {target-size} KB | {improvement-size} KB ({percentage}%) | {progress}% |

**Status:**
- ✅ Target met: {metrics-that-met-target}
- ⚠️ Improved but target not met: {metrics-improved-but-not-at-target}
- ❌ Regressed: {metrics-that-regressed}
```

### Step 9.4 – Verify Target Metrics

Check if all target metrics were achieved:

- **All targets met:** Proceed to Step 9.5 (create result report)
- **Some targets not met but improvement achieved:** Proceed to Step 9.5, but flag in Jira comment
- **Any metric regressed:** Execute the recovery procedure below before stopping.

#### Regression Recovery Procedure

If any metric is worse than the baseline value, perform these steps in order:

**Step 9.4.1 – Save regression context**

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

**Step 9.4.2 – Stash working directory changes**

```bash
git stash push -m "perf-regression-stash: {jira-key} at {timestamp}"
```

**Only stash uncommitted working tree changes** — do NOT run `git reset`. At this point in the
workflow (Step 9, before Step 10 commits), no commit has been made yet. The stash preserves all
modified files so the developer can inspect them with `git stash show -p` or recover them with
`git stash pop`.

**Step 9.4.3 – Inform user**

> ❌ **Performance regression detected — changes stashed**
>
> The optimization caused a regression in {metric-name}:
> - Baseline: {baseline-value}
> - Current: {current-value}
> - Change: {delta} (regression)
>
> **Your code changes have been stashed** (not lost):
> - View changes: `git stash show -p`
> - Restore to investigate: `git stash pop`
> - Discard entirely: `git stash drop`
>
> **Regression report saved to:** `.claude/performance/optimization-results/{jira_key}-regression-{timestamp}.md`
>
> Fix the regression and re-run `/sdlc-workflow:performance-implement-optimization {jira-key}` to try again.

Stop execution.

### Step 9.5 – Create Optimization Result Report

After capturing current performance metrics and validating no regressions, create an optimization result report for audit trail and verification:

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

| Metric | Baseline (p95) | After Optimization (p95) | Delta | Target | Status |
|---|---|---|---|---|---|
| LCP | {baseline-lcp}ms | {current-lcp}ms | {delta-lcp} | {target-lcp}ms | {status-lcp} |
| FCP | {baseline-fcp}ms | {current-fcp}ms | {delta-fcp} | {target-fcp}ms | {status-fcp} |
| DOM Interactive | {baseline-dom}ms | {current-dom}ms | {delta-dom} | {target-dom}ms | {status-dom} |
| Total Load Time | {baseline-total}ms | {current-total}ms | {delta-total} | {target-total}ms | {status-total} |

**Performance Summary:**
- {summary-line: e.g., "LCP improved by 300ms (9.4%), 62% to target"}

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

ℹ️  Configuration will be updated after PR merge: re-run /sdlc-workflow:performance-baseline on main branch
```

**Note:** This approach eliminates race conditions by writing to isolated per-task report files instead of shared config. The configuration's "Latest Verified" column is updated by re-running baseline on main after each PR merge, ensuring it always reflects the actual current state.

## Step 10 – Commit Changes

(Same as implement-task Step 11, with performance note)

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

(Same as implement-task Step 12)

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

(Extension to implement-task Step 13)

Post a comment to the Jira task with:
1. PR link
2. Performance test results (before/after comparison table)
3. Status of target achievement

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

Update the Jira task custom field with the PR link:

```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py update_issue {task-id} \
    --fields-json '{"customfield_10875": "{pr-url}"}'
```

Discover available transitions and transition the task to "In Review":

```bash
# Get available transitions for the task
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py get_transitions {task-id}

# Parse output to find "In Review" transition ID
# Example output: [{"id": "51", "name": "In Review"}, {"id": "31", "name": "Done"}]
# Extract the ID where name matches "In Review"

# Transition using discovered ID
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py transition_issue {task-id} \
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
