---
name: performance-implement-optimization
description: |
  Execute performance optimization task by implementing code changes, running performance tests, and comparing results against targets.
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
  python3 plugins/sdlc-workflow/scripts/jira-client.py get_issue {task-id} --fields "*all"
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

1. Copy the capture script from plugin cache to a temporary location:
   ```bash
   cp plugins/sdlc-workflow/skills/performance/capture-baseline.template.mjs /tmp/capture-baseline-current.mjs
   chmod +x /tmp/capture-baseline-current.mjs
   ```

2. Run the capture script with mode-specific parameters:
   ```bash
   # If cold-start mode:
   node /tmp/capture-baseline-current.mjs --config {path-to-performance-config.md} --port {port} --mode cold-start
   
   # If e2e mode:
   node /tmp/capture-baseline-current.mjs --config {path-to-performance-config.md} --mode e2e --e2e-command "{e2e-command}"
   
   # If both mode:
   node /tmp/capture-baseline-current.mjs --config {path-to-performance-config.md} --port {port} --mode both --e2e-command "{e2e-command}"
   ```

3. Parse the JSON output to extract current metrics (LCP, FCP, TTI, Total Load Time, bundle size)

**Compare metrics:** Before (original baseline) vs After (new baseline) using same mode for accurate comparison.

### Step 9.2 – Compare Against Baseline and Targets

Read the Baseline Metrics and Target Metrics from the Jira task description (parsed in Step 2).

For each metric (LCP, FCP, TTI, bundle size):
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
| TTI (p95) | {baseline-tti} ms | {current-tti} ms | {target-tti} ms | {improvement-tti} ms ({percentage}%) | {progress}% |
| Bundle Size | {baseline-size} KB | {current-size} KB | {target-size} KB | {improvement-size} KB ({percentage}%) | {progress}% |

**Status:**
- ✅ Target met: {metrics-that-met-target}
- ⚠️ Improved but target not met: {metrics-improved-but-not-at-target}
- ❌ Regressed: {metrics-that-regressed}
```

### Step 9.4 – Verify Target Metrics

Check if all target metrics were achieved:

- **All targets met:** Proceed to Step 10 (commit and PR)
- **Some targets not met but improvement achieved:** Proceed to Step 10, but flag in Jira comment
- **Any metric regressed:** Stop and inform user. Do not proceed with commit/PR.

If a metric regressed, inform the user:

> ❌ **Performance regression detected!**
>
> The optimization caused a regression in {metric-name}:
> - Baseline: {baseline-value}
> - Current: {current-value}
> - Change: {change} (regression)
>
> Please review the implementation and identify the cause of the regression before proceeding.

Stop execution.

### Step 9.3.5 – Update Configuration with Current Metrics (New)

After capturing current performance metrics and validating no regressions, update the performance-config.md with the latest values:

**Step 9.3.5.1 – Read Current Configuration**

Read `.claude/performance-config.md` from the target repository.

**Step 9.3.5.2 – Update Optimization Targets Table**

Update the **Current (p95)** column in the Optimization Targets section:

| Metric | Baseline (p95) | Current (p95) | Target | Unit | Last Updated |
|---|---|---|---|---|---|
| LCP | {unchanged} | **{current-lcp-p95 from Step 9.3}** | {unchanged} | seconds | **{timestamp}** |
| FCP | {unchanged} | **{current-fcp-p95}** | {unchanged} | seconds | **{timestamp}** |
| TTI | {unchanged} | **{current-tti-p95}** | {unchanged} | seconds | **{timestamp}** |
| Total Load Time | {unchanged} | **{current-total-p95}** | {unchanged} | seconds | **{timestamp}** |

- Leave **Baseline (p95)** column unchanged (baseline is immutable)
- Update **Current (p95)** column with p95 metrics from Step 9.1 capture
- Keep **Target** column unchanged
- Set **Last Updated** = current timestamp

**Step 9.3.5.3 – Update Metadata**

Update the metadata section:

```yaml
metadata:
  # ... existing fields ...
  last_updated: {current-timestamp}
```

**Step 9.3.5.4 – Write Updated Configuration**

Write the updated configuration back to `.claude/performance-config.md`.

**Step 9.3.5.5 – Log Configuration Update**

Log to user:

```
✓ Configuration auto-updated with current metrics:
  - LCP (p95): {baseline} → {current} ({improvement-percentage}%)
  - FCP (p95): {baseline} → {current} ({improvement-percentage}%)
  - TTI (p95): {baseline} → {current} ({improvement-percentage}%)
  - Total Load Time (p95): {baseline} → {current} ({improvement-percentage}%)
  - Last updated: {timestamp}
```

**Note:** This step keeps the configuration in sync with optimization progress, enabling tracking of incremental improvements across multiple optimization tasks.

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

Assisted-by: Claude Sonnet 4.5 <noreply@anthropic.com>
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
  python3 plugins/sdlc-workflow/scripts/jira-client.py update_issue {task-id} \
    --fields-json '{"customfield_10875": "{pr-url}"}'
```

Transition the task to "In Review":

```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  python3 plugins/sdlc-workflow/scripts/jira-client.py transition_issue {task-id} \
    --transition-id 51
```

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
