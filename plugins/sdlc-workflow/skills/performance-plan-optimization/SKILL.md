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

**Validate repository type based on analysis scope:**

1. **Check if performance-config.md exists:**
   - If exists: Read `metadata.analysis_scope` field
   - If not exists: Skip validation (setup hasn't run yet, proceed to Step 2)

2. **Conditional validation based on scope:**

   **If `analysis_scope = "backend-only"`:**
   - Verify backend repository indicators exist:
     - Rust: `Cargo.toml`, `src/main.rs` or `src/lib.rs`
     - Java: `pom.xml` or `build.gradle`, `src/main/java/`
     - Python: `requirements.txt` or `pyproject.toml`, Python files
     - Node: `package.json` with server dependencies (express, fastify, etc.)
     - Ruby: `Gemfile`, `.rb` files
     - C#: `.csproj`, `.cs` files
   - **Skip frontend indicator validation**

   **If `analysis_scope = "frontend-only"`:**
   - Verify frontend application indicators exist:
     - `package.json` with frontend dependencies
     - `src/` or `app/` directory
     - Frontend framework indicators (React, Vue, Angular, Svelte, Next.js configuration files)
   - **Skip backend indicator validation**

   **If `analysis_scope = "full-stack"` or `"full-stack-monorepo"`:**
   - **Verify BOTH frontend AND backend indicators exist**
   - Frontend indicators (same as frontend-only above)
   - Backend indicators (same as backend-only above)
   - Both must be present for full-stack analysis

   **If config doesn't exist:**
   - Skip validation entirely (setup phase hasn't completed)
   - Proceed to Step 2

## Step 2 – Verify Performance Configuration Exists

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Verify config exists, stop if missing
- Extract: Selected workflow name
- Extract: Target directories (plans directory location)

## Step 3 – Resolve Analysis Report Path

**Apply:** [Common Pattern: Directory Extraction](../performance/common-patterns.md#pattern-4-directory-extraction)

**Specific directory to extract:**
- `analysis_dir` → Analysis directory path (e.g., `.claude/performance/analysis/`)

**Specific actions for this skill:**
- Construct analysis report path: `{analysis_dir}/workflow-analysis-report.md`
- Store path for validation in Step 4 (do not check existence here)

## Step 4 – Read and Parse Analysis Report

Read the analysis report at `{analysis-directory}/workflow-analysis-report.md`.

**Validation checks:**

1. **Check if report file exists:**
   ```bash
   if [ ! -f "$report_file" ]; then
     error: "Analysis report not found at expected location.
     
     Please run /sdlc-workflow:performance-analyze-module first to generate
     the analysis report, then re-run this skill."
     exit 1
   fi
   ```

2. **Check for required sections:**
   ```bash
   if ! grep -q "## Anti-Pattern Analysis" "$report_file"; then
     error: "Analysis report incomplete (missing Anti-Pattern Analysis section).
     
     The report may be corrupted or from an old version.
     Please re-run /sdlc-workflow:performance-analyze-module to regenerate
     the analysis report."
     exit 1
   fi
   ```

3. **Parse anti-pattern counts and check if any exist:**
   
   Parse the Anti-Pattern Analysis section and sum all instance counts.
   
   ```
   total_instances = sum(all anti-pattern instance counts)
   
   if total_instances == 0:
     warn:
     > ℹ️ **No anti-patterns detected in analysis report**
     >
     > Performance may already be optimal, or analysis coverage was limited
     > (e.g., backend not available, limited frontend inspection).
     >
     > **Options:**
     > 1. Proceed with plan creation (will create Epic with note about optimal state)
     > 2. Cancel and re-run analysis with broader scope
     >
     > Choose (1/2):
   ```
   
   If user chooses "2. Cancel", stop execution.
   
   If user chooses "1. Proceed", continue but note in Epic description that no anti-patterns were detected.

**If validation passes, extract the following data:**

**Workflow metrics:**
- Workflow name
- Current performance metrics (LCP p95, FCP p95, DOM Interactive p95, Total Load Time p95)
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

Store this data for use in Steps 5, 6, 7, and 8.

## Step 5 – Conduct Cross-Functional Impact Analysis

Before grouping optimizations into tasks, analyze the potential impact of each optimization on other functionalities in the application. This step ensures performance improvements don't break existing features or degrade user experience in other workflows.

**Apply:** [Common Pattern: Code Intelligence Strategy](../performance/common-patterns.md#pattern-9-code-intelligence-strategy-serena-first-with-grep-fallback)

**Key Principle:** Always use Serena MCP first for code analysis, with Grep as fallback strategy.

### Step 5.1 – Identify Affected Code Modules

For each optimization recommendation from the analysis report (extracted in Step 4):

**Extract optimization metadata:**
- File paths and line numbers from anti-pattern findings
- Code locations (component names, handler functions, class names)
- Optimization type (bundle size, render, backend query, caching, etc.)

**Use Serena-first strategy (Pattern 9) to find usage:**

```python
# FIRST CHOICE: Serena MCP (if available from CLAUDE.md Repository Registry)
if serena_available:
    try:
        # Find all references to affected component/function
        affected_usage = mcp__serena__find_referencing_symbols(
            symbol_name=affected_component_name,
            relative_path="src/"
        )
        method_used = "Serena MCP"
        confidence = "High"
        log: f"✅ Found {len(affected_usage)} references via Serena MCP"
    except (ToolNotFoundError, Exception) as e:
        log: f"⚠️ Serena MCP failed: {e}, falling back to Grep"
        # Fall through to Grep fallback

# FALLBACK STRATEGY: Grep search
if method_used != "Serena MCP":
    # Search for imports and usage patterns
    grep -r "import.*{affected_component}" src/
    grep -r "from.*{affected_file}.*import" src/
    grep -r "{affected_function}(" src/
    method_used = "Grep (Fallback)"
    confidence = "Medium"
    log: "ℹ️ Using Grep fallback (pattern matching only)"
```

**Classify impact scope:**

Based on the number of files/components found:

- **Isolated**: Single file/component (no other files import or reference it)
- **Low**: 2-3 files in same module/layer
- **Medium**: 4-7 files OR cross-layer (e.g., frontend component + backend API)
- **High**: ≥8 files OR core infrastructure (routing, authentication, state management, database schema)

**Document which method was used:**
```
optimization_analysis[optimization_name] = {
    "detection_method": method_used,  # "Serena MCP" | "Grep (Fallback)"
    "confidence": confidence,          # "High" | "Medium"
    "affected_files_count": count,
    "impact_scope": scope              # "Isolated" | "Low" | "Medium" | "High"
}
```

### Step 5.2 – Assess Cross-Functional Impact Severity

For each optimization with scope ≥ Low (not Isolated):

**Count affected workflows:**
- Search for workflow entry points (route components, page components) that import affected code
- Cross-reference with workflows defined in performance-config.md
- Count distinct workflows using the affected code

**Classify impact severity:**

- **None**: No other workflows affected (isolated to target workflow only)
- **Low**: 1-2 workflows affected beyond target workflow
- **Medium**: 3-4 workflows affected
- **High**: 5-10 workflows affected
- **Critical**: All workflows affected OR changes to core business logic/shared infrastructure

**Identify risk factors:**

Categorize the type of impact:

| Risk Factor | Description | Examples |
|---|---|---|
| **Breaking Change** | Breaks existing functionality | API contract change, response schema modification, removed function parameter |
| **Behavioral Change** | Alters behavior without breaking | Different sort order, caching changes data freshness, retry logic changes |
| **Performance Trade-off** | Improves one metric, may degrade another | Caching reduces latency but increases memory, lazy loading reduces initial bundle but delays feature access |
| **Cosmetic Change** | Affects only visual presentation | Styling changes, layout shifts, animation timing |
| **Infrastructure Change** | Requires new infrastructure | Adding Redis, database migration, new service dependency |

**Document severity assessment:**
```
optimization_analysis[optimization_name].update({
    "affected_workflows": [list of workflow names],
    "affected_workflows_count": count,
    "severity": severity,  # "Critical" | "High" | "Medium" | "Low" | "None"
    "risk_factors": [list of identified risks]
})
```

### Step 5.3 – Make Rational Decision

Apply the decision framework to determine whether to proceed with each optimization:

**Decision Framework:**

```
Decision = f(Performance Benefit, Impact Scope, Impact Severity)

Rules (evaluated in order):

1. IF Scope = Isolated AND Severity = None
   → RECOMMEND (safe, no blast radius)

2. IF Benefit ≥ 20% AND Scope ≤ Medium AND Severity ≤ Medium
   → RECOMMEND (high benefit, manageable risk)

3. IF Benefit ≥ 10% AND Benefit < 20% AND Scope ≤ Low AND Severity ≤ Medium
   → RECOMMEND WITH CAUTION (moderate benefit, extra testing required)

4. IF Benefit ≥ 20% AND Scope = Medium AND Severity = High
   → RECOMMEND WITH CAUTION (high benefit justifies high risk, but needs safeguards)

5. IF Benefit ≥ 20% AND Scope = High AND Severity = Critical
   → CONDITIONAL (high benefit but requires infrastructure/process not yet in place)

6. IF Benefit < 10% AND Severity ≥ High
   → DEFER (risk outweighs benefit)

7. IF Risk Factor includes "Infrastructure Change" AND infrastructure not deployed
   → CONDITIONAL (need to deploy infrastructure first)

8. IF Benefit < 5% AND Scope ≥ Medium
   → REJECT (minimal benefit, not worth risk)

9. DEFAULT → DEFER (unclear risk/benefit, needs manual review)
```

**Decision Outcomes:**

- **RECOMMEND**: Create Jira task with standard process
  - Safe optimization with acceptable risk/benefit ratio
  - Proceed with implementation using normal workflow

- **RECOMMEND WITH CAUTION**: Create Jira task + add safeguards
  - High-benefit optimization with medium-high risk
  - Required safeguards:
    - Feature flag for gradual rollout
    - Regression testing for all affected workflows
    - Staging environment validation before production
    - Detailed rollback plan

- **CONDITIONAL**: Document requirements, do NOT create task yet
  - Prerequisites not met (e.g., Redis not deployed, feature flag system not available)
  - Conditions must be satisfied before optimization can proceed
  - Document what needs to happen first

- **DEFER**: Document for future review, do NOT create task
  - Risk currently outweighs benefit
  - May be reconsidered when:
    - Infrastructure improves
    - Risk mitigation becomes available
    - Benefit threshold increases

- **REJECT**: Document reasoning, do NOT create task
  - Risk far outweighs benefit
  - Not recommended to pursue
  - Document alternative approaches if available

### Step 5.4 – Document Impact Analysis

For each optimization, create a structured impact analysis document:

```markdown
### Optimization: {optimization-name}

**Performance Benefit:** {quantified-impact} ({percentage}% improvement)  
**Estimated Impact:** {time-savings-ms} ms or {size-reduction-kb} KB

**Cross-Functional Impact Analysis:**
- **Detection Method:** {Serena MCP | Grep (Fallback)}
- **Confidence:** {High | Medium | Low}
- **Impact Scope:** {Isolated | Low | Medium | High}
- **Impact Severity:** {Critical | High | Medium | Low | None}

**Affected Components:**
- `{component-path-1}` — Used by {workflow-count} workflows
- `{component-path-2}` — Shared utility function
- `{handler-path}` — Backend API handler

**Affected Workflows:**
- {workflow-1} — {how it's affected}
- {workflow-2} — {how it's affected}
- {workflow-3} — {how it's affected}

**Risk Factors:**
- {risk-factor-1} — {description}
- {risk-factor-2} — {description}

**Decision:** {RECOMMEND | RECOMMEND WITH CAUTION | CONDITIONAL | DEFER | REJECT}

**Rationale:** {Detailed reasoning for the decision, explaining how the decision framework was applied}

**Required Safeguards:** (if RECOMMEND WITH CAUTION)
- Feature flag `PERF_OPT_{FEATURE_NAME}` for gradual rollout (0% → 10% → 50% → 100%)
- Regression test suite for workflows: {list}
- Load testing with 2x expected traffic
- Monitoring alerts for: {metrics}
- Rollback trigger: Any Core Web Vital degrades >10% OR error rate increases >2%

**Prerequisites:** (if CONDITIONAL)
- {prerequisite-1}
- {prerequisite-2}
- Estimated time to satisfy prerequisites: {estimate}

**Conditions for Reconsideration:** (if DEFER)
- {condition-1}
- {condition-2}
- Re-evaluate when: {trigger}

**Alternative Approaches:** (if REJECT)
- {alternative-1}
- {alternative-2}
```

**Store impact analysis for use in Steps 6-9:**

Keep all impact analysis data in memory for:
- Step 6: Filter optimizations by decision (only RECOMMEND + RECOMMEND WITH CAUTION become tasks)
- Step 7: Include impact analysis in optimization plan document
- Step 9: Include impact assessment in Jira task descriptions
- Step 10: Include risk profile in Jira Epic description

## Step 6 – Group Optimizations into Logical Tasks

Group the **RECOMMENDED** and **RECOMMEND WITH CAUTION** optimizations into logical tasks.

**Important:** Only optimizations with decisions **RECOMMEND** or **RECOMMEND WITH CAUTION** are grouped into tasks. CONDITIONAL, DEFER, and REJECT optimizations are documented in the optimization plan but do NOT become Jira tasks.

**Filtering Logic:**

1. **Filter optimizations by decision:**
   ```python
   task_optimizations = [opt for opt in all_optimizations 
                         if opt.decision in ["RECOMMEND", "RECOMMEND WITH CAUTION"]]
   ```

2. **If all optimizations filtered out (no RECOMMEND or RECOMMEND WITH CAUTION):**
   - Create Epic with summary note
   - Document: "No optimization tasks created at this time. See optimization plan for deferred/conditional items."
   - Add comment to Epic listing all deferred/conditional/rejected optimizations with rationale
   - Skip to Step 11 (Output Summary) with note about deferred optimizations

3. **If at least one optimization passes filter:**
   - Proceed with task grouping using LAYER+TYPE taxonomy below
   - Include impact analysis data in task descriptions

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

## Step 7 – Generate Optimization Plan Document

Create the optimization plan document at `{plans-directory}/optimization-plan.md`.

### Step 7.1 – Determine Plan Location

Read the **Target Directories** section from performance-config.md and extract the plans directory path (e.g., `.claude/performance/plans/`).

Construct the plan filename: `optimization-plan.md`

### Step 7.2 – Plan Document Structure

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
- DOM Interactive (p95): {current-domInteractive} ms (Target: 3500 ms)
- Total Load Time (p95): {current-total} ms (Target: 4000 ms)

**Expected Impact:**
- Estimated LCP improvement: {lcp-improvement} ms ({lcp-percentage}% reduction)
- Estimated FCP improvement: {fcp-improvement} ms ({fcp-percentage}% reduction)
- Estimated DOM Interactive improvement: {domInteractive-improvement} ms ({domInteractive-percentage}% reduction)
- Estimated bundle size reduction: {bundle-size-reduction} KB

**Total Effort Estimate:** {total-effort-days} days

---

## Impact Analysis Summary

**Total Optimizations Evaluated:** {total-count}  
**Recommended:** {recommend-count} optimizations → {task-count} tasks  
**Recommended with Caution:** {caution-count} optimizations (extra safeguards required)  
**Conditional:** {conditional-count} optimizations (prerequisites not met)  
**Deferred:** {defer-count} optimizations (documented for future review)  
**Rejected:** {reject-count} optimizations (risk > benefit)

### Decision Distribution

| Decision | Count | Reason |
|---|---|---|
| RECOMMEND | {recommend-count} | Safe, high-benefit optimizations |
| RECOMMEND WITH CAUTION | {caution-count} | High benefit but medium-high risk, extra safeguards required |
| CONDITIONAL | {conditional-count} | Prerequisites not met (infrastructure, feature flags, etc.) |
| DEFER | {defer-count} | Risk currently outweighs benefit |
| REJECT | {reject-count} | Not worth pursuing |

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

## Deferred and Rejected Optimizations

### Deferred for Future Review

{For each DEFER or CONDITIONAL decision:}

#### {optimization-name}

**Performance Benefit:** {quantified-impact} ({percentage}% improvement)  
**Decision:** {DEFERRED | CONDITIONAL}  
**Reason:** {why deferred or what prerequisites are missing}

**Impact Analysis:**
- **Impact Scope:** {scope}
- **Impact Severity:** {severity}
- **Affected Workflows:** {list}
- **Risk Factors:** {list}

**Conditions for Reconsideration:**
- {condition-1}
- {condition-2}

{If CONDITIONAL, list prerequisites:}
**Prerequisites:**
- {prerequisite-1}
- {prerequisite-2}
- **Estimated time to satisfy:** {estimate}

---

### Rejected Optimizations

{For each REJECT decision:}

#### {optimization-name}

**Performance Benefit:** {quantified-impact} ({percentage}% improvement)  
**Decision:** REJECTED  
**Reason:** {why rejected - explain risk/benefit analysis}

**Impact Analysis:**
- **Impact Scope:** {scope}
- **Impact Severity:** {severity}
- **Risk Factors:** {list}

**Rationale:** {detailed explanation of why risk far outweighs benefit}

**Alternative Approaches:** (if any)
- {alternative-1}
- {alternative-2}

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

### Step 7.3 – Calculate Expected Impact

For each metric (LCP, FCP, DOM Interactive, bundle size):
- Sum the estimated improvements from all optimizations
- Calculate percentage reduction: `(improvement / current) * 100`
- Ensure estimates are conservative (use lower bound of impact range)

### Step 7.4 – Calculate Total Effort

Map effort labels to days:
- Low effort: 0.5 day
- Medium effort: 2 days
- High effort: 5 days

Sum across all tasks to get total effort estimate.

### Step 7.5 – Write Plan Document

Write the generated plan to `{plans-directory}/optimization-plan.md`.

## Step 8 – Create Jira Epic for Optimization Work

Create a Jira Epic to group all optimization tasks.

### Step 8.1 – Construct Epic Summary and Description

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
- DOM Interactive improvement: {domInteractive-improvement} ms ({domInteractive-percentage}% reduction)
- Bundle size reduction: {bundle-size-reduction} KB

## Risk Profile

**Total Optimizations Evaluated:** {total-optimizations}  
**Tasks Created:** {task-count}  
**Deferred:** {defer-count} optimizations (documented for future)  
**Rejected:** {reject-count} optimizations (risk > benefit)

**Risk Distribution:**
- Safe optimizations (RECOMMEND): {recommend-count} tasks
- Caution-required optimizations (RECOMMEND WITH CAUTION): {caution-count} tasks — extra safeguards needed

{If deferred-count > 0:}
**Note:** See optimization plan document for {defer-count} deferred optimizations and rationale for future reconsideration.

{If conditional-count > 0:}
**Conditional Optimizations:** {conditional-count} optimizations require prerequisites (infrastructure deployment, feature flags, etc.) before they can be implemented.

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

### Step 8.2 – Create Epic via Jira

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
    cd <plugin-root> && python3 scripts/jira-client.py create_issue \
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

### Step 8.3 – Capture Epic Key

After Epic creation (via MCP or REST API), extract the Epic key (e.g., `TC-5001`) from the response.

Store the Epic key for use in Step 8 (task creation and linking).

## Step 9 – Create Jira Tasks for Each Optimization

For each grouped optimization task (from Step 6), create a Jira Task.

### Step 9.1 – Construct Task Description

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
- **DOM Interactive (p95):** {current-domInteractive} ms
- **Bundle Size:** {current-bundle-size} KB

## Target Metrics

- **LCP (p95):** < {target-lcp} ms
- **FCP (p95):** < {target-fcp} ms
- **DOM Interactive (p95):** < {target-domInteractive} ms
- **Bundle Size:** < {target-bundle-size} KB

## Implementation Notes

{specific-guidance}

## Cross-Functional Impact Assessment

**Decision:** {RECOMMEND | RECOMMEND WITH CAUTION}  
**Impact Scope:** {Isolated | Low | Medium | High}  
**Impact Severity:** {Critical | High | Medium | Low | None}  
**Detection Method:** {Serena MCP | Grep (Fallback)}  
**Confidence:** {High | Medium | Low}

**Affected Workflows:**
- {workflow-1} — {how affected}
- {workflow-2} — {how affected}

**Affected Components:**
- `{component-path}` — Used by {workflow-count} workflows
- `{utility-path}` — Shared utility

**Risk Factors:**
- {risk-factor-1}
- {risk-factor-2}

**Required Safeguards:** {if RECOMMEND WITH CAUTION}
- Feature flag: `PERF_OPT_{FEATURE_NAME}` for gradual rollout (0% → 10% → 50% → 100%)
- Staging environment validation required before production
- Rollback plan: {specific rollback steps}
- Monitoring alerts for: {metrics to watch}
- Rollback trigger: Any Core Web Vital degrades >10% OR error rate increases >2%

**Testing Requirements for Affected Workflows:**
- [ ] Test target workflow ({workflow-name}) with optimization
- [ ] Regression test affected workflows: {list}
- [ ] Performance baseline capture for workflows: {list}
- [ ] Load testing if backend changes (2x expected traffic)
- [ ] Visual regression testing if UI changes

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

### Step 9.2 – Create Task via Jira

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

### Step 9.3 – Set Epic as Parent of Task

Set the Epic as the **parent** of the Task using Jira's hierarchy field. This is the correct
relationship for Epic→Task in Jira Cloud/Data Center: it makes tasks appear in the Epic's backlog
and board view. A "Relates" issue link creates only a peer reference and does NOT establish the
hierarchy.

**Attempt 1: Use Atlassian MCP with parent field**

```
jira.create_issue(
  ...task fields...,
  parent=<epic-key>   ← pass Epic key as parent when creating the task
)
```

If the MCP `create_issue` call supports a `parent` field, set it to the Epic key at task creation
time (Step 9.2). This is more reliable than a separate link call.

**Attempt 2: Update parent field after creation (if not set at creation)**

If the task was created without a parent, update it:

```
jira.update_issue(
  issue_key=<task-key>,
  fields={"parent": {"key": <epic-key>}}
)
```

**REST API fallback:**

```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py update_issue {task-key} \
    --fields-json '{"parent": {"key": "{epic-key}"}}'
```

**If parent field is unsupported (older Jira versions):**

Fall back to `Epic Link` custom field (Jira Software classic):

```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py update_issue {task-key} \
    --fields-json '{"customfield_10014": "{epic-key}"}'
```

**Note:** `customfield_10014` is the standard Jira `Epic Link` field ID. Confirm the correct
field ID for your instance with:
```bash
JIRA_SERVER_URL="{url}" JIRA_EMAIL="{email}" JIRA_API_TOKEN="{token}" \
  cd <plugin-root> && python3 scripts/jira-client.py get_fields | grep -i epic
```

### Step 9.4 – Link Tasks with Dependencies

For tasks with dependencies (e.g., Task 2 depends on Task 1), create "Blocks" links.

**Link structure:**
- Task 1 (prerequisite) **blocks** Task 2 (dependent)

**Create link:**
```
jira.create_issue_link(
  inward_issue=<task-1-key>,
  outward_issue=<task-2-key>,
  link_type="Blocks"
)
```

## Step 10 – Post Optimization Plan as Comment on Epic

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
    cd <plugin-root> && python3 scripts/jira-client.py add_comment {epic-key} \
      --comment-md "{plan-content}"
  ```

Append the skill footer to the comment:

```markdown
---

This comment was AI-generated by [sdlc-workflow/performance-plan-optimization](https://github.com/mrizzi/sdlc-plugins) v{version}.
```

## Step 11 – Output Summary

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
- Task descriptions must include performance-specific sections (Baseline Metrics, Target Metrics, Performance Test Requirements, Cross-Functional Impact Assessment)
- Plan document saved locally even if Jira operations fail
- **Impact Analysis (Step 5) is mandatory** — always conduct cross-functional impact analysis before task grouping
- **Use Serena MCP first** (Pattern 9) for code analysis, fallback to Grep only when Serena unavailable
- **Document analysis method** — always record whether Serena MCP or Grep was used, with confidence level
- **Filter by decision** — only RECOMMEND and RECOMMEND WITH CAUTION optimizations become Jira tasks
- **If all optimizations deferred/rejected** — create Epic with summary, document deferred items in plan, add comment to Epic listing all deferred optimizations with rationale
- **If Serena MCP unavailable** — log informative message, use Grep fallback, add confidence note to impact analysis
- **If impact analysis fails for an optimization** — default decision to DEFER, document "Manual review required", continue with remaining optimizations
- **Deferred/Rejected optimizations** — must be documented in optimization plan with rationale and conditions for reconsideration
- **Decision rationale** — every optimization decision (RECOMMEND/CAUTION/CONDITIONAL/DEFER/REJECT) must include transparent reasoning based on decision framework
- **Risk profile** — Epic description must include risk distribution (safe vs caution-required tasks, deferred count)
