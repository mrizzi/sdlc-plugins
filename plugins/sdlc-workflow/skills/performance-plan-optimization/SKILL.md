---
name: performance-plan-optimization
description: |
  Read analysis reports and generate structured optimization plan with Jira Epic and Tasks. Does NOT analyze source code — organizes findings from performance-analyze-module.
argument-hint: "[target-repository-path]"
---

# performance-plan-optimization skill

You are an AI optimization planning assistant. You generate a structured optimization plan by **reading** module-level analysis reports (created by `performance-analyze-module`), grouping optimization recommendations into logical tasks, creating Jira Epic and Tasks for optimization work, and producing an optimization-plan.md document with sequenced implementation steps.

**Key Distinction:** This skill does NOT inspect source code. It reads the analysis report from `performance-analyze-module` and organizes the findings into actionable Jira tasks.

## Guardrails

- This skill creates files in designated performance directories (`.claude/performance/plans/`)
- This skill does NOT modify source code files — only creates planning artifacts and Jira issues
- This skill requires an existing workflow-analysis-report.md from the analyze-module skill

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

Verify the target directory exists and contains a frontend application (check for `package.json`, `src/`, or similar frontend indicators).

## Step 2 – Verify Performance Configuration Exists

Check if `.claude/performance-config.md` exists in the target repository.

- **If not exists:** Inform the user:
  > "Performance Analysis Configuration not found. Please run `/sdlc-workflow:performance-setup` first to initialize the configuration, then re-run this skill."
  
  Stop execution.

- **If exists:** Read the configuration file and extract:
  - Selected workflow name
  - Target directories (plans directory location)

## Step 3 – Verify Analysis Report Exists

Determine the analysis report location from the configuration file:

Look for the **Target Directories** section and extract the analysis directory path (e.g., `.claude/performance/analysis/`).

Construct the analysis report filename: `workflow-analysis-report.md`

Check if the file exists at `{analysis-directory}/workflow-analysis-report.md`.

- **If analysis report does not exist:** Inform the user:
  > "Analysis report not found. Please run `/sdlc-workflow:performance-analyze-module` first to generate the analysis report, then re-run this skill."
  
  Stop execution.

- **If analysis report exists:** Proceed to Step 4.

## Step 4 – Read and Parse Analysis Report

Read the analysis report at `{analysis-directory}/workflow-analysis-report.md`.

Extract the following data:

**Workflow metrics:**
- Workflow name
- Current performance metrics (LCP p95, FCP p95, TTI p95, Total Load Time p95)
- Target metrics
- Overall performance rating

**Anti-pattern findings:**
- For each anti-pattern detected:
  - Anti-pattern name
  - Severity (High/Medium/Low)
  - Instances found (count)
  - Estimated impact (time or size savings)
  - Code locations (file paths and line numbers)
  - Recommended fixes

**Prioritized optimizations:**
- Optimization recommendations sorted by impact
- Effort estimates (Low/Medium/High)

Store this data for use in Steps 5, 6, and 7.

## Step 5 – Group Optimizations into Logical Tasks

Group the optimization recommendations into logical tasks based on optimization category:

### Task Grouping Strategy

Optimizations are categorized by **LAYER** and **TYPE** to support full-stack performance optimization.

**LAYER 1: Frontend Optimizations**

- **Category 1A: Bundle Size Reduction**
  - Code splitting optimizations
  - Tree shaking improvements
  - Lazy loading implementations
  - Dead code elimination

- **Category 1B: Render Optimization**
  - Component memoization (React.memo, useMemo, useCallback)
  - Virtual scrolling for large lists
  - Avoid layout thrashing (batch DOM operations)
  - Long task mitigation (Web workers, async patterns)

- **Category 1C: Resource Optimization**
  - Eliminate render-blocking resources (async/defer scripts, async CSS)
  - Parallel resource loading
  - Image compression and lazy loading

**LAYER 2: Backend Optimizations** (only when backend repository is configured)

- **Category 2A: Query Optimization**
  - Eliminate database N+1 queries (batch queries, eager loading)
  - Add pagination to unbounded endpoints
  - Optimize inefficient queries (specific column selection, add indexes)

- **Category 2B: Response Optimization**
  - Reduce over-fetching (create specialized DTOs, GraphQL)
  - Add caching for expensive operations (Redis, in-memory)

**LAYER 3: Integration Optimizations** (cross-cutting frontend/backend)

- **Category 3A: API Communication**
  - Batch multiple API calls into single requests
  - Parallel fetching (replace sequential with parallel)
  - Implement caching strategy (client-side cache with revalidation)

### Task Structure

For each group, create a task with:
- **Task summary:** "{Category}: {Brief Description}"
- **Description:** What optimizations are included and why
- **Files to modify:** List of files affected by this optimization group
- **Baseline metrics:** Current performance metrics for this workflow
- **Target metrics:** Expected metrics after optimization
- **Acceptance criteria:** Pass/fail checklist for each optimization
- **Performance test requirements:** How to verify the optimization worked
- **Dependencies:** Which tasks must be completed first

### Task Sequencing Rules

Order tasks by:
1. **Quick wins first** — Low effort, high impact optimizations
2. **Dependencies** — Tasks that unblock other tasks go first
3. **Risk** — Low-risk changes before high-risk changes

## Step 6 – Generate Optimization Plan Document

Create the optimization plan document at `{plans-directory}/optimization-plan.md`.

### Step 6.1 – Determine Plan Location

Read the **Target Directories** section from performance-config.md and extract the plans directory path (e.g., `.claude/performance/plans/`).

Construct the plan filename: `optimization-plan.md`

### Step 6.2 – Plan Document Structure

```markdown
# Performance Optimization Plan

**Workflow:** {workflow-name}  
**Generated:** {iso-8601-timestamp}  
**Overall Rating:** {current-rating} → Target: Excellent

---

## Executive Summary

**Current State:**
- LCP (p95): {current-lcp} ms (Target: 2500 ms)
- FCP (p95): {current-fcp} ms (Target: 1800 ms)
- TTI (p95): {current-tti} ms (Target: 3500 ms)
- Total Load Time (p95): {current-total} ms (Target: 4000 ms)

**Expected Impact:**
- Estimated LCP improvement: {lcp-improvement} ms ({lcp-percentage}% reduction)
- Estimated FCP improvement: {fcp-improvement} ms ({fcp-percentage}% reduction)
- Estimated TTI improvement: {tti-improvement} ms ({tti-percentage}% reduction)
- Estimated bundle size reduction: {bundle-size-reduction} KB

**Total Effort Estimate:** {total-effort-days} days

---

## Task Sequence

| # | Task | Category | Impact | Effort | Dependencies |
|---|---|---|---|---|---|
| 1 | {task-1-summary} | {category-1} | {impact-1} | {effort-1} | None |
| 2 | {task-2-summary} | {category-2} | {impact-2} | {effort-2} | Task 1 |
| ... | ... | ... | ... | ... | ... |

---

## Task Details

### Task 1: {task-1-summary}

**Category:** {category}  
**Impact:** {quantified-impact}  
**Effort:** {effort-estimate}  
**Risk:** {High / Medium / Low}

**Description:**
{what-this-task-achieves}

**Files to Modify:**
- `{file-path-1}` — {reason}
- `{file-path-2}` — {reason}

**Baseline Metrics:**
- LCP: {current-lcp} ms
- Bundle size: {current-bundle-size} KB

**Target Metrics:**
- LCP: < {target-lcp} ms
- Bundle size: < {target-bundle-size} KB

**Acceptance Criteria:**
- [ ] {criterion-1}
- [ ] {criterion-2}

**Performance Test Requirements:**
- [ ] Re-run baseline capture after implementation
- [ ] Verify LCP improvement of at least {improvement} ms
- [ ] Ensure no regressions in other metrics

**Dependencies:** {prerequisite-tasks}

**Rollback Strategy:** {how-to-undo-if-needed}

---

{... repeat for each task ...}

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| {risk-1} | {likelihood} | {impact} | {mitigation-strategy} |
| {risk-2} | {likelihood} | {impact} | {mitigation-strategy} |
| ... | ... | ... | ... |

**Common Risks:**
- **Breaking changes:** Optimizations may introduce regressions. Mitigation: Comprehensive testing before merging.
- **Performance measurement noise:** Baseline variability may obscure small improvements. Mitigation: Run multiple baseline iterations.
- **Third-party library constraints:** Some optimizations may be blocked by library limitations. Mitigation: Evaluate alternative libraries.

---

## Rollback Strategy

If an optimization causes issues:

1. **Immediate rollback:** Revert the commit and redeploy previous version
2. **Root cause analysis:** Investigate what caused the issue
3. **Revised approach:** Update the optimization plan and re-attempt with fixes
4. **Re-baseline:** Capture new baseline to measure impact of rollback

---

## Next Steps

1. **Review this plan** with the team and adjust task sequencing if needed
2. **Create Jira Epic and Tasks** — This skill will create these automatically
3. **Implement tasks** in sequence using `/sdlc-workflow:implement-task {task-id}`
4. **Re-baseline after each task** using `/sdlc-workflow:performance-baseline` to measure improvements
5. **Final verification** using `/sdlc-workflow:performance-verify-optimization` to validate all targets met
```

### Step 6.3 – Calculate Expected Impact

For each metric (LCP, FCP, TTI, bundle size):
- Sum the estimated improvements from all optimizations
- Calculate percentage reduction: `(improvement / current) * 100`
- Ensure estimates are conservative (use lower bound of impact range)

### Step 6.4 – Calculate Total Effort

Map effort labels to days:
- Low effort: 0.5 day
- Medium effort: 2 days
- High effort: 5 days

Sum across all tasks to get total effort estimate.

### Step 6.5 – Write Plan Document

Write the generated plan to `{plans-directory}/optimization-plan.md`.

## Step 7 – Create Jira Epic for Optimization Work

Create a Jira Epic to group all optimization tasks.

### Step 7.1 – Construct Epic Summary and Description

**Epic Summary:**
```
Performance Optimization: {workflow-name}
```

**Epic Description (Markdown):**
```markdown
# Performance Optimization Epic

**Workflow:** {workflow-name}  
**Current Rating:** {current-rating}  
**Target Rating:** Excellent

## Executive Summary

This Epic tracks performance optimization work for the {workflow-name} workflow. Optimizations are grouped into {task-count} tasks with an estimated total effort of {total-effort-days} days.

**Expected Impact:**
- LCP improvement: {lcp-improvement} ms ({lcp-percentage}% reduction)
- FCP improvement: {fcp-improvement} ms ({fcp-percentage}% reduction)
- TTI improvement: {tti-improvement} ms ({tti-percentage}% reduction)
- Bundle size reduction: {bundle-size-reduction} KB

## Tasks

{task-count} optimization tasks have been created and linked to this Epic. Implement them in sequence to achieve the target performance metrics.

**Task Sequence:**
1. {task-1-summary} — {impact-1}, {effort-1}
2. {task-2-summary} — {impact-2}, {effort-2}
...

See the full optimization plan in the comments below.

---

_This Epic was AI-generated by [sdlc-workflow/performance-plan-optimization](https://github.com/mrizzi/sdlc-plugins) v{version}._
```

### Step 7.2 – Create Epic via Jira

**Attempt 1: Use Atlassian MCP**

Try to create the Epic using Atlassian MCP:
```
jira.create_issue(
  project_key=<project-key>,
  summary=<epic-summary>,
  description=<epic-description>,
  issue_type="Epic",
  labels=["ai-generated-jira", "performance-optimization", <workflow-name>]
)
```

**If MCP fails:**

Prompt the user with the standard fallback flow (see `shared/jira-access-strategy.md`):

> ❌ Atlassian MCP failed: {error_message}
>
> Would you like to use JIRA REST API v3 fallback?
>
> Options:
> 1. Yes - Use REST API (requires credentials)
> 2. No - Skip Jira Epic creation
> 3. Retry - I'll fix MCP configuration and retry
>
> Choose (1/2/3):

**If user chooses "1. Yes":**
- Check CLAUDE.md for existing REST API credentials
- If credentials exist: use them
- If not: collect credentials, validate, and store
- Create Epic via REST API:
  ```bash
  JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
    python3 plugins/sdlc-workflow/scripts/jira-client.py create_issue \
      --project {project-key} \
      --summary "{epic-summary}" \
      --description-md "{epic-description}" \
      --issue-type Epic \
      --labels ai-generated-jira performance-optimization {workflow-name}
  ```

**If user chooses "2. No":**
- Skip Jira Epic creation
- Continue with local plan file only
- Inform user: "Optimization plan saved locally. You can create the Epic manually later."
- Skip to Step 9 (plan document saved, no Jira operations)

**If user chooses "3. Retry":**
- Retry MCP operation once
- If retry fails, offer fallback options again

### Step 7.3 – Capture Epic Key

After Epic creation (via MCP or REST API), extract the Epic key (e.g., `TC-5001`) from the response.

Store the Epic key for use in Step 8 (task creation and linking).

## Step 8 – Create Jira Tasks for Each Optimization

For each grouped optimization task (from Step 5), create a Jira Task.

### Step 8.1 – Construct Task Description

Use the task-description-template.md structure, extending with performance-specific sections:

```markdown
## Repository

{repository-name}

## Description

{task-description}

## Files to Modify

- `{file-path}` — {reason}

## Baseline Metrics

- **LCP (p95):** {current-lcp} ms
- **FCP (p95):** {current-fcp} ms
- **TTI (p95):** {current-tti} ms
- **Bundle Size:** {current-bundle-size} KB

## Target Metrics

- **LCP (p95):** < {target-lcp} ms
- **FCP (p95):** < {target-fcp} ms
- **TTI (p95):** < {target-tti} ms
- **Bundle Size:** < {target-bundle-size} KB

## Implementation Notes

{specific-guidance}

## Acceptance Criteria

- [ ] {criterion-1}
- [ ] {criterion-2}
- [ ] Re-run baseline capture shows improvement in target metrics
- [ ] No regressions in other performance metrics

## Performance Test Requirements

- [ ] Run `/sdlc-workflow:performance-baseline` after implementation
- [ ] Verify {metric} improvement of at least {improvement}
- [ ] Run `/sdlc-workflow:performance-verify-optimization` to validate targets

## Dependencies

{prerequisite-tasks}
```

### Step 8.2 – Create Task via Jira

For each task:

**Attempt 1: Use Atlassian MCP**

```
jira.create_issue(
  project_key=<project-key>,
  summary=<task-summary>,
  description=<task-description>,
  issue_type="Task",
  labels=["ai-generated-jira", "performance-optimization", <workflow-name>, <layer>, <category>]
)
```

**Label structure:**
- `<layer>`: "frontend" | "backend" | "integration"
- `<category>`: Derived from task grouping:
  - Frontend: "bundle-size", "render-optimization", "resource-optimization"
  - Backend: "query-optimization", "response-optimization"
  - Integration: "api-communication"

**Example:** For a backend database N+1 optimization task:
```
labels=["ai-generated-jira", "performance-optimization", "product-catalog", "backend", "query-optimization"]
```

**If MCP fails:**
- Use the same fallback flow as Epic creation (Step 7.2)
- Create via REST API if user consents

**Capture Task Key:**
- Extract the task key (e.g., `TC-5002`) from the response
- Store for linking in Step 8.3

### Step 8.3 – Link Task to Epic

Create an "Incorporates" link between the Epic and the Task.

**Attempt 1: Use Atlassian MCP**

```
jira.create_link(
  inward_issue=<epic-key>,
  outward_issue=<task-key>,
  link_type="Incorporates"
)
```

**If MCP fails:**
- Use REST API fallback:
  ```bash
  JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
    python3 plugins/sdlc-workflow/scripts/jira-client.py create_link \
      --inward {epic-key} \
      --outward {task-key} \
      --link-type Incorporates
  ```

### Step 8.4 – Link Tasks with Dependencies

For tasks with dependencies (e.g., Task 2 depends on Task 1), create "Blocks" links.

**Link structure:**
- Task 1 (prerequisite) **blocks** Task 2 (dependent)

**Create link:**
```
jira.create_link(
  inward_issue=<task-2-key>,
  outward_issue=<task-1-key>,
  link_type="Blocks"
)
```

## Step 9 – Post Optimization Plan as Comment on Epic

Read the optimization plan document at `{plans-directory}/optimization-plan.md`.

Post the plan content as a comment on the Epic issue.

**Attempt 1: Use Atlassian MCP**

```
jira.add_comment(
  issue_key=<epic-key>,
  comment=<plan-content>
)
```

**If MCP fails:**
- Use REST API fallback:
  ```bash
  JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
    python3 plugins/sdlc-workflow/scripts/jira-client.py add_comment {epic-key} \
      --comment-md "{plan-content}"
  ```

Append the skill footer to the comment:

```markdown
---

This comment was AI-generated by [sdlc-workflow/performance-plan-optimization](https://github.com/mrizzi/sdlc-plugins) v{version}.
```

## Step 10 – Output Summary

Report to the user:

> ✅ **Optimization plan created successfully!**
>
> **Workflow:** {workflow-name}  
> **Expected Impact:**
> - LCP improvement: {lcp-improvement} ms ({lcp-percentage}% reduction)
> - FCP improvement: {fcp-improvement} ms ({fcp-percentage}% reduction)
> - Bundle size reduction: {bundle-size-reduction} KB
>
> **Optimization Plan:** `.claude/performance/plans/optimization-plan.md`
>
> **Jira Epic:** {epic-key} — "Performance Optimization: {workflow-name}"  
> **Tasks Created:** {task-count} tasks
> - {task-1-key}: {task-1-summary}
> - {task-2-key}: {task-2-summary}
> - ...
>
> **Total Effort Estimate:** {total-effort-days} days
>
> **Next Steps:**
>
> 1. Review the optimization plan and Jira tasks with your team
> 2. Implement tasks in sequence:
>    ```
>    /sdlc-workflow:implement-task {task-1-key}
>    ```
> 3. After each task, re-run baseline to measure improvement:
>    ```
>    /sdlc-workflow:performance-baseline
>    ```

If Jira Epic/Tasks were not created (user chose "No" in fallback), adjust the summary:

> ✅ **Optimization plan created successfully!**
>
> **Workflow:** {workflow-name}  
> **Plan location:** `.claude/performance/plans/optimization-plan.md`
>
> **Note:** Jira Epic and Tasks were not created. You can create them manually from the plan document.

## Important Rules

- Never modify source code files — only create planning artifacts and Jira issues
- Always verify analysis report exists before proceeding
- Group optimizations into logical tasks with clear boundaries (not one task per anti-pattern)
- Task sequencing must follow dependencies (quick wins first, then dependent tasks)
- All Jira issues must include `ai-generated-jira` label
- Effort estimates should be conservative (use upper bound of effort range)
- Risk assessment must include mitigation strategies
- Rollback strategy must be included for all tasks
- If Jira operations fail and user declines REST API, save plan locally and continue
- Use Atlassian MCP first, fallback to REST API only with user consent
- Epic issue type must be used for grouping optimization tasks
- Task descriptions must include performance-specific sections (Baseline Metrics, Target Metrics, Performance Test Requirements)
- Plan document saved locally even if Jira operations fail
