# Performance Skills Common Patterns

This document defines reusable patterns used across all performance skills to ensure consistency and reduce duplication.

## Pattern 1: Config Reading

**Purpose:** Validate that `performance-config.md` exists before skill execution

**When to use:** All skills (typically Step 2)

**Used by:**
- performance-baseline (Step 2)
- performance-analyze-module (Step 2)
- performance-plan-optimization (Step 2)
- performance-implement-optimization (Step 1)
- performance-verify-optimization (Step 6.1)
- performance-setup (Step 2 - detection only)

**Procedure:**

```bash
# Check for performance configuration
if [ ! -f ".claude/performance-config.md" ]; then
  echo "Performance Analysis Configuration not found."
  echo "Please run /sdlc-workflow:performance-setup first."
  exit 1
fi

# Read configuration
config=$(cat .claude/performance-config.md)
```

**Error handling:**

If config does not exist, inform the user:

> "Performance Analysis Configuration not found. Please run `/sdlc-workflow:performance-setup` first to initialize the configuration, then re-run this skill."

Stop execution.

**Variations:**

- **setup skill**: Checks if config exists to offer update vs skip (Step 2)
- **Other skills**: Config must exist or skill fails

---

## Pattern 2: Metadata Extraction

**Purpose:** Read metadata fields from performance-config.md frontmatter

**When to use:** Skills that need baseline_mode, backend_available, e2e_test_path, baseline_commit_sha, or other metadata

**Used by:**
- performance-baseline (Step 2.2)
- performance-analyze-module (Step 2.2)
- performance-implement-optimization (Step 9.0.5, Step 9.1)
- performance-verify-optimization (Step 6.2)
- performance-setup (Step 2 - version detection)

**Procedure:**

```bash
# Check for metadata frontmatter (v2 config)
if config starts with "---\nmetadata:":
  config_version = 2
  extract metadata.baseline_mode (cold-start | e2e | both | null)
  extract metadata.baseline_captured (true | false)
  extract metadata.baseline_timestamp (ISO timestamp | null)
  extract metadata.baseline_commit_sha (git SHA | null)
  extract metadata.backend_available (true | false)
  extract metadata.e2e_test_path (path | null)
  extract metadata.e2e_coverage (true | false)
  extract metadata.last_updated (ISO timestamp)
else:
  # v1 config without metadata
  config_version = 1
  # Use defaults or fall back to alternative extraction methods
```

**Metadata Fields Reference:**

| Field | Type | Description | Default (v1) |
|---|---|---|---|
| `version` | string | Config version identifier | "1.0" |
| `created` | ISO timestamp | When config was first created | file mtime |
| `last_updated` | ISO timestamp | When config was last modified | file mtime |
| `config_schema_version` | integer | Schema version (1 or 2) | 1 |
| `workflow_selected` | boolean | Whether workflow has been selected | true if Selected Workflow exists |
| `baseline_captured` | boolean | Whether initial baseline was captured | Check if baseline report exists |
| `baseline_mode` | string or null | Capture mode (cold-start, e2e, both) | null or extract from baseline report |
| `baseline_timestamp` | ISO timestamp or null | When baseline was captured | null |
| `baseline_commit_sha` | string or null | Git commit at baseline capture | null |
| `backend_available` | boolean | Whether backend is configured and accessible | false |
| `e2e_test_path` | string or null | Path to e2e test for selected workflow | null |
| `e2e_coverage` | boolean | Whether selected workflow has e2e test | false |

**Error handling:**

- If metadata is missing but expected (config_version = 1), offer auto-migration to v2
- If metadata is malformed, log warning and use defaults

---

## Pattern 3: Mode Consistency Enforcement

**Purpose:** Ensure all baseline captures use the same mode for valid performance comparisons

**When to use:** When capturing performance metrics (baseline, implement re-run, verify re-run)

**Used by:**
- performance-baseline (Step 3.0, Step 3.1)
- performance-implement-optimization (Step 9.1)
- performance-verify-optimization (Step 6.2)

**Procedure:**

```bash
# Read stored mode from metadata (see Pattern 2)
stored_mode = metadata.baseline_mode  # null | "cold-start" | "e2e" | "both"
baseline_already_captured = metadata.baseline_captured  # true | false

# If baseline already captured, enforce mode consistency
if baseline_already_captured and stored_mode is not null:
  # Inform user of stored mode
  echo "Previous baseline mode detected: ${stored_mode}"
  echo "For valid comparisons, all captures MUST use the same mode."
  
  # If user tries to select different mode, warn:
  if user_selected_mode != stored_mode:
    echo "⚠️ Mode mismatch detected!"
    echo "Stored mode: ${stored_mode}"
    echo "Selected mode: ${user_selected_mode}"
    echo ""
    echo "Options:"
    echo "1. Use stored mode (${stored_mode}) - Recommended"
    echo "2. Reset baseline (discards previous baseline)"
    echo "3. Cancel"
    
    # Handle user choice
    if choice == 1:
      user_selected_mode = stored_mode
    elif choice == 2:
      # Clear baseline data, allow new mode
      metadata.baseline_captured = false
      metadata.baseline_mode = null
    else:
      exit 0
fi

# Use user_selected_mode for capture
mode = user_selected_mode
```

**Why consistency matters:**

Different modes measure different conditions:
- **cold-start**: Direct URL navigation with cold cache (worst-case, first visit)
- **e2e**: Test automation with warm cache (realistic user workflow)
- **both**: Runs e2e first, then cold-start (comprehensive)

Comparing metrics across different modes produces invalid results.

**Error handling:**

- If user chooses mode different from stored mode, warn and offer reset or cancel
- If mode is null (first capture), store user's selection in metadata

---

## Pattern 4: Directory Extraction

**Purpose:** Extract performance artifact directories from configuration

**When to use:** When writing performance reports (baseline, analysis, plans, verification)

**Used by:**
- performance-baseline (Step 8.1)
- performance-analyze-module (Step 7.1)
- performance-plan-optimization (Step 6.1)
- performance-implement-optimization (Step 9.1)
- performance-verify-optimization (Step 6.3)

**Procedure:**

```bash
# Read Target Directories section from config
target_directories=$(grep -A 10 "## Target Directories" .claude/performance-config.md)

# Extract directory paths
baseline_dir=$(echo "$target_directories" | grep "baselines" | awk '{print $4}')
analysis_dir=$(echo "$target_directories" | grep "analysis" | awk '{print $4}')
plans_dir=$(echo "$target_directories" | grep "plans" | awk '{print $4}')
verification_dir=$(echo "$target_directories" | grep "verification" | awk '{print $4}')

# Standard paths (from template)
baseline_dir=".claude/performance/baselines/"
analysis_dir=".claude/performance/analysis/"
plans_dir=".claude/performance/plans/"
verification_dir=".claude/performance/verification/"

# Ensure directories exist
mkdir -p "$baseline_dir" "$analysis_dir" "$plans_dir" "$verification_dir"
```

**Standard directory structure:**

```
.claude/performance/
├── baselines/           # Baseline performance reports
├── analysis/            # Module and application analysis reports
├── plans/               # Optimization plan documents
└── verification/        # Verification reports for optimization PRs
```

**Error handling:**

- If directory creation fails (permissions issue), stop execution
- If Target Directories section is missing, use standard paths

---

## Pattern 5: Version Detection

**Purpose:** Detect configuration schema version (v1 vs v2) and offer auto-migration

**When to use:** Early in skill execution (typically Step 2)

**Used by:**
- performance-setup (Step 2)
- performance-baseline (Step 2.2)
- performance-analyze-module (Step 2.2)
- performance-implement-optimization (Step 9.0.5)

**Procedure:**

```bash
# Read first lines of config to check for metadata frontmatter
config_header=$(head -n 20 .claude/performance-config.md)

# Detect version
if echo "$config_header" | grep -q "^---$"; then
  # Check if metadata section exists
  if echo "$config_header" | grep -q "metadata:"; then
    # v2 config
    config_version=2
    schema_version=$(echo "$config_header" | grep "config_schema_version:" | awk '{print $2}')
  else:
    # Has frontmatter but no metadata - malformed
    config_version=1
  fi
else:
  # No frontmatter - v1 config
  config_version=1
fi

# If v1, offer migration
if [ "$config_version" -eq 1 ]; then
  echo "ℹ️ Configuration upgrade available"
  echo ""
  echo "Your config is v1 (pre-metadata). Upgrade to v2 for:"
  echo "- Baseline mode consistency enforcement"
  echo "- Auto-update of optimization metrics"
  echo "- Backend availability caching"
  echo "- Baseline freshness tracking"
  echo ""
  echo "Upgrade now? (yes/no)"
  echo ""
  echo "Your original config will be backed up to:"
  echo ".claude/performance-config.md.v1.backup"
  
  read -p "> " upgrade_choice
  
  if [ "$upgrade_choice" = "yes" ]; then
    # Run migration (see Migration Pattern)
    migrate_v1_to_v2
  else:
    echo "Continuing with v1 config (some features disabled)"
  fi
fi
```

**Version differences:**

| Feature | v1 Config | v2 Config |
|---|---|---|
| Metadata frontmatter | ❌ No | ✅ Yes |
| Baseline mode storage | Only in baseline report | In config metadata |
| Backend availability caching | Re-validated each time | Cached in metadata |
| Config auto-update | ❌ No | ✅ Yes (baseline, implement) |
| Baseline freshness check | ❌ No | ✅ Yes (commit SHA tracking) |
| E2E test path storage | ❌ No | ✅ Yes (metadata) |
| Optimization Targets format | 2-column (Target, Unit) | 3-column (Baseline, Current, Target) |

**Error handling:**

- If migration fails, continue with v1 (degraded mode warnings)
- If metadata is malformed, treat as v1

---

## Pattern 6: Baseline Report Reading

**Purpose:** Read baseline metrics from baseline-report.md

**When to use:** When comparing current performance against baseline

**Used by:**
- performance-analyze-module (Step 3)
- performance-plan-optimization (Step 3)
- performance-implement-optimization (Step 9.1, Step 9.2)

**Procedure:**

```bash
# Check if baseline report exists
baseline_report=".claude/performance/baselines/baseline-report.md"

if [ ! -f "$baseline_report" ]; then
  echo "Baseline report not found. Please run /sdlc-workflow:performance-baseline first."
  exit 1
fi

# Read baseline report
report=$(cat "$baseline_report")

# Extract p95 metrics from Performance Metrics section
lcp_p95=$(echo "$report" | grep "LCP (p95)" | awk '{print $4}')
fcp_p95=$(echo "$report" | grep "FCP (p95)" | awk '{print $4}')
tti_p95=$(echo "$report" | grep "TTI (p95)" | awk '{print $4}')
total_load_p95=$(echo "$report" | grep "Total Load Time (p95)" | awk '{print $4}')

# Extract capture mode from frontmatter
capture_mode=$(echo "$report" | grep "capture_mode:" | awk '{print $2}')

# Extract baseline timestamp
baseline_timestamp=$(echo "$report" | grep "timestamp:" | awk '{print $2}')
```

**Baseline Report Structure:**

```markdown
---
workflow: {workflow-name}
timestamp: {ISO-timestamp}
capture_mode: cold-start | e2e | both
commit_sha: {git-commit-sha}
---

# Baseline Performance Report

## Performance Metrics

| Metric | p50 | p75 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| LCP | ... | ... | ... | ... | ms |
| FCP | ... | ... | ... | ... | ms |
| TTI | ... | ... | ... | ... | ms |
| Total Load Time | ... | ... | ... | ... | ms |
```

**Error handling:**

- If baseline report is missing, stop execution with actionable message
- If metrics are malformed, log warning and use fallback values

---

## Pattern 7: Workflow Validation

**Purpose:** Extract and validate Selected Workflow section from configuration

**When to use:** When skill operates on a specific workflow (most skills)

**Used by:**
- performance-baseline (Step 2.1)
- performance-analyze-module (Step 2.1)
- performance-plan-optimization (Step 2.1)
- performance-implement-optimization (Step 2)

**Procedure:**

```bash
# Check for Selected Workflow section
if ! grep -q "## Selected Workflow" .claude/performance-config.md; then
  echo "No workflow selected for optimization."
  echo "Please run /sdlc-workflow:performance-setup first to select a workflow."
  exit 1
fi

# Extract workflow details
workflow_section=$(grep -A 20 "## Selected Workflow" .claude/performance-config.md)

workflow_name=$(echo "$workflow_section" | grep "Workflow Name" | awk -F'|' '{print $3}' | xargs)
entry_point=$(echo "$workflow_section" | grep "Entry Point" | awk -F'|' '{print $3}' | xargs)
key_screens=$(echo "$workflow_section" | grep "Key Screens" | awk -F'|' '{print $3}' | xargs)
complexity=$(echo "$workflow_section" | grep "Complexity" | awk -F'|' '{print $3}' | xargs)
selected_on=$(echo "$workflow_section" | grep "Selected On" | awk -F'|' '{print $3}' | xargs)

# Store for later use
export WORKFLOW_NAME="$workflow_name"
export ENTRY_POINT="$entry_point"
export KEY_SCREENS="$key_screens"
export COMPLEXITY="$complexity"
```

**Selected Workflow Table Format:**

```markdown
## Selected Workflow

The following workflow has been selected for performance optimization:

| Property | Value |
|---|---|
| Workflow Name | {workflow-name} |
| Entry Point | {entry-point-url} |
| Key Screens | {comma-separated-list} |
| Complexity | {complexity-estimate} |
| Selected On | {YYYY-MM-DD} |
```

**Error handling:**

- If Selected Workflow section is missing, stop execution
- If workflow details are incomplete, warn user and attempt to proceed with available data

---

## Migration Pattern: V1 to V2 Config Upgrade

**Purpose:** Upgrade v1 config (no metadata) to v2 config (with metadata frontmatter)

**When to use:** When Pattern 5 (Version Detection) identifies v1 config and user agrees to upgrade

**Procedure:**

```bash
# Backup original config
cp .claude/performance-config.md .claude/performance-config.md.v1.backup

# Read existing config
config=$(cat .claude/performance-config.md)

# Extract baseline mode from baseline report (if exists)
baseline_mode="null"
baseline_captured="false"
baseline_commit_sha="null"
baseline_timestamp="null"

if [ -f ".claude/performance/baselines/baseline-report.md" ]; then
  baseline_captured="true"
  baseline_mode=$(grep "capture_mode:" .claude/performance/baselines/baseline-report.md | awk '{print $2}')
  baseline_commit_sha=$(grep "commit_sha:" .claude/performance/baselines/baseline-report.md | awk '{print $2}')
  baseline_timestamp=$(grep "timestamp:" .claude/performance/baselines/baseline-report.md | awk '{print $2}')
fi

# Check if workflow is selected
workflow_selected="false"
if grep -q "## Selected Workflow" .claude/performance-config.md; then
  workflow_selected="true"
fi

# Check if backend is available
backend_available="false"
backend_path=$(grep "Backend Path" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
if [ -n "$backend_path" ] && [ -d "$backend_path" ]; then
  backend_available="true"
fi

# Create metadata frontmatter
current_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
file_mtime=$(stat -c %Y .claude/performance-config.md 2>/dev/null || stat -f %m .claude/performance-config.md)
created_timestamp=$(date -u -d "@$file_mtime" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -r $file_mtime +"%Y-%m-%dT%H:%M:%SZ")

metadata="---
metadata:
  version: 1.0
  created: ${created_timestamp}
  last_updated: ${current_timestamp}
  config_schema_version: 2
  workflow_selected: ${workflow_selected}
  baseline_captured: ${baseline_captured}
  baseline_mode: ${baseline_mode}
  baseline_timestamp: ${baseline_timestamp}
  baseline_commit_sha: ${baseline_commit_sha}
  backend_available: ${backend_available}
  e2e_test_path: null
  e2e_coverage: false
---
"

# Prepend metadata to config
echo "$metadata" > .claude/performance-config.md.tmp
echo "" >> .claude/performance-config.md.tmp
cat .claude/performance-config.md >> .claude/performance-config.md.tmp
mv .claude/performance-config.md.tmp .claude/performance-config.md

# Update Optimization Targets section to 3-column format
# (Implementation depends on sed/awk skills - simplified here)
# TODO: Transform 2-column table to 3-column with Baseline/Current/Target

# Add Backend Available field to Backend Configuration section
# TODO: Add "Backend Available | ${backend_available} | Cached validation status" row

echo "✅ Configuration upgraded to v2"
echo "Backup saved to: .claude/performance-config.md.v1.backup"
```

**Migration checklist:**

- [x] Create metadata frontmatter with defaults
- [x] Extract baseline mode from existing baseline report (if exists)
- [x] Validate backend path and set backend_available flag
- [x] Check if workflow is selected (workflow_selected flag)
- [ ] Transform Optimization Targets to 3-column format (Baseline/Current/Target)
- [ ] Add "Backend Available" row to Backend Configuration table
- [x] Backup original config to .v1.backup

---

## Usage Guidelines

### When to create a new pattern

Create a new pattern when:
- The same logic appears in 3+ skills
- The logic is complex enough to warrant standardization (>10 lines)
- The logic has error handling that should be consistent

### When NOT to create a pattern

Do not create a pattern when:
- The logic is skill-specific (unique to one skill)
- The logic is trivial (1-2 lines)
- The logic has high variability across skills

### Referencing patterns in skills

**Format:**

```markdown
## Step X – {Step Title}

**Apply:** [Common Pattern: {Pattern Name}](../performance/common-patterns.md#pattern-N-{pattern-slug})

**Specific actions for this skill:**
- Extract: {skill-specific detail}
- Validate: {skill-specific check}
- Store: {skill-specific variable}
```

**Example:**

```markdown
## Step 2 – Verify Performance Configuration Exists

**Apply:** [Common Pattern: Config Reading](../performance/common-patterns.md#pattern-1-config-reading)

**Specific actions for this skill:**
- Extract: Selected Workflow section
- Extract: Baseline Capture Settings
- Validate: Workflow has key screens defined
```

---

## Maintenance

**When updating a pattern:**

1. Update the pattern definition in this file
2. Verify all skills referencing the pattern still work correctly
3. Update pattern version history (if significant change)
4. Test end-to-end workflow with updated pattern

**Pattern versioning:**

Patterns are not formally versioned. Breaking changes to patterns should be avoided. If a breaking change is necessary:
1. Create a new pattern (Pattern N+1)
2. Migrate skills gradually
3. Mark old pattern as deprecated
4. Remove old pattern after all skills migrated
