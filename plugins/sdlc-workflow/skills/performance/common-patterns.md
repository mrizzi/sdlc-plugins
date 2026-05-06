# Performance Skills Common Patterns

This document defines reusable patterns used across all performance skills to ensure consistency and reduce duplication.

## Pattern 0: Plugin Root Resolution

**Purpose:** Locate the installed sdlc-workflow plugin root directory at runtime

**When to use:** Once per skill, before any operation that reads plugin files (scripts, templates, shared resources)

**Used by:**
- All skills that use Jira REST API fallback (Pattern 11)
- Skills that read plugin templates or scripts

**Procedure:**

```bash
# Resolve plugin root — works for any registry name and any version
plugin_root=$(ls -d "${HOME}/.claude/plugins/cache/"*/sdlc-workflow/*/ 2>/dev/null \
  | sort -V | tail -1)

if [ -z "$plugin_root" ] || [ ! -d "$plugin_root" ]; then
  echo "❌ sdlc-workflow plugin not found in ~/.claude/plugins/cache/"
  echo "   Ensure the plugin is installed and try again."
  exit 1
fi

# $plugin_root is now set, e.g.: /home/user/.claude/plugins/cache/sdlc-plugins-local/sdlc-workflow/0.6.1/
```

**Why this works:**

- Glob `cache/*/sdlc-workflow/*/` matches any registry name (sdlc-plugins-local, sdlc-plugins, marketplace names)
- Matches any version number in the plugin cache
- `sort -V | tail -1` selects the latest version if multiple are present
- Uses `$HOME` for cross-platform compatibility
- Validation ensures the directory exists before proceeding

**Usage in subsequent commands:**

```bash
# Reference a template path (use agent Read tool on this path)
template_path="${plugin_root}skills/performance/performance-config.template.md"

# Execute plugin script
python3 "$plugin_root/scripts/jira-client.py" <command>
```

---

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


**Used by:**
- performance-baseline (Step 2.2)
- performance-analyze-module (Step 2.2)
- performance-implement-optimization (Step 9.0.5, Step 9.1)
- performance-verify-optimization (Step 6.2)
- performance-setup (Step 2 - version detection)

**Procedure:**

```bash
# Read metadata from frontmatter
extract metadata.baseline_captured (true | false)
extract metadata.baseline_timestamp (ISO timestamp | null)
extract metadata.baseline_commit_sha (git SHA | null)
extract metadata.backend_available (true | false)
extract metadata.last_updated (ISO timestamp)
```

**Metadata Fields Reference:**

| Field | Type | Description |
|---|---|---|
| `version` | string | Config version identifier |
| `created` | ISO timestamp | When config was first created |
| `last_updated` | ISO timestamp | When config was last modified |
| `workflow_selected` | boolean | Whether workflow has been selected |
| `baseline_captured` | boolean | Whether initial baseline was captured |
| `baseline_timestamp` | ISO timestamp or null | When baseline was captured |
| `baseline_commit_sha` | string or null | Git commit at baseline capture |
| `backend_available` | boolean | Whether backend is configured and accessible |
| `analysis_scope` | string | Determines which repositories are analyzed: "full-stack-monorepo" (same repo), "full-stack" (separate repos), "frontend-only", "backend-only" |

**Error handling:**

- If metadata is malformed, log warning and use defaults

---

## Pattern 3: Mode Consistency Enforcement

**Purpose:** Ensure all baseline captures use the same mode for valid performance comparisons

**When to use:** When capturing performance metrics (baseline, implement re-run, verify re-run)

**Used by:**
- performance-baseline (Step 5.0, Step 5.1)
- performance-implement-optimization (Step 9.1)
- performance-verify-optimization (Step 6.2)

**Procedure:**

```bash
# Read stored mode from metadata (see Pattern 2)
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
- performance-analyze-module (Steps 7.1-A/B)
- performance-plan-optimization (Step 6.1)
- performance-implement-optimization (Step 9.1)
- performance-verify-optimization (Step 6.3)

**Procedure:**

```bash
# Read Target Directories section from config
target_directories=$(grep -A 10 "## Target Directories" .claude/performance-config.md)

# Standard directory paths
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

## Pattern 5: Baseline Report Reading

**Purpose:** Read baseline metrics from baseline-report.md

**When to use:** When comparing current performance against baseline

**Used by:**
- performance-analyze-module (Step 3)
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
tti_p95=$(echo "$report" | grep "DOM Interactive (p95)" | awk '{print $4}')
total_load_p95=$(echo "$report" | grep "Total Load Time (p95)" | awk '{print $4}')

# Extract metadata from YAML frontmatter (between --- delimiters)
frontmatter=$(echo "$report" | sed -n '/^---$/,/^---$/p' | sed '1d;$d')
workflow_name=$(echo "$frontmatter" | grep "workflow:" | awk '{print $2}')
capture_mode=$(echo "$frontmatter" | grep "capture_mode:" | awk '{print $2}')

# Extract baseline timestamp
baseline_timestamp=$(echo "$report" | grep "timestamp:" | awk '{print $2}')
```

**Baseline Report Structure:**

```markdown
---
workflow: {workflow-name}
timestamp: {ISO-timestamp}
commit_sha: {git-commit-sha}
---

# Baseline Performance Report

## Performance Metrics

| Metric | p50 | p75 | p95 | p99 | Unit |
|---|---|---|---|---|---|
| LCP | ... | ... | ... | ... | ms |
| FCP | ... | ... | ... | ... | ms |
| DOM Interactive | ... | ... | ... | ... | ms |
| Total Load Time | ... | ... | ... | ... | ms |
```

**Error handling:**

- If baseline report is missing, stop execution with actionable message
- If metrics are malformed, log warning and use fallback values

---

## Pattern 6: Workflow Validation

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

## Pattern 7: Dev Command Approval

**Purpose:** Discover, present, and get user approval for dev mode commands before execution

**When to use:** Before baseline capture when application needs to be running

**Used by:**
- performance-baseline (Step 7.4)
- performance-implement-optimization (Step 9 - before re-running baseline)
- performance-verify-optimization (Step 6 - before re-running baseline)

**Procedure:**

```bash
# Step 1: Check if dev command already configured
if grep -q "## Development Environment" .claude/performance-config.md; then
  dev_command=$(grep "Dev Command" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
  command_approved=$(grep "dev_command_approved:" .claude/performance-config.md | awk '{print $2}')
  command_hash=$(grep "dev_command_hash:" .claude/performance-config.md | awk '{print $2}' | tr -d '"')
  
  # Calculate current hash
  current_hash=$(echo -n "$dev_command" | sha256sum | awk '{print $1}')
  
  # If command unchanged and already approved, skip prompt
  if [ "$command_approved" = "true" ] && [ "$current_hash" = "$command_hash" ]; then
    echo "ℹ️ Dev command already approved: $dev_command"
    skip_to_verification=true
  fi
fi

# Step 2: If not approved or changed, discover dev command
if [ "$skip_to_verification" != "true" ]; then
  discovered_command=""
  doc_source=""
  
  # Check package.json scripts
  if [ -f "package.json" ]; then
    dev_script=$(jq -r '.scripts.dev // .scripts.start // .scripts.serve // "null"' package.json)
    if [ "$dev_script" != "null" ]; then
      discovered_command="npm run dev"
      doc_source="package.json scripts.dev"
    fi
  fi
  
  # If not found, prompt manually
  if [ -z "$discovered_command" ]; then
    echo "⚠️ Could not auto-discover dev command from package.json"
    echo "Please enter the command to start your application:"
    read -p "> " discovered_command
    doc_source="Manual user input"
  fi
fi

# Step 3: Extract port number (simple detection)
port=""

# From .env file
if [ -f ".env" ]; then
  port=$(grep "^PORT=" .env | cut -d= -f2)
fi

# Framework default fallback
if [ -z "$port" ]; then
  if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    port=3000
  elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
    port=5173
  elif [ -f "manage.py" ]; then
    port=8000
  else
    port=3000  # Default
  fi
fi

# Step 4: Prompt user for approval
echo ""
echo "ℹ️ Development Mode Command Discovered"
echo ""
echo "Command: $discovered_command"
echo "Source: $doc_source"
echo "Port: $port"
echo ""
echo "What would you like to do?"
echo ""
echo "1. Approve - Use this command as-is"
echo "2. Modify - Make changes to the command"
echo "3. Exit - Cancel and exit skill"
echo ""
read -p "Choose (1/2/3): " choice

case $choice in
  1)
    final_command="$discovered_command"
    echo "✅ Using command: $final_command"
    ;;
  2)
    echo ""
    echo "Enter the modified command:"
    read -p "> " user_modifications
    if [ -z "$user_modifications" ]; then
      echo "❌ No command provided. Exiting."
      exit 1
    fi
    final_command="$user_modifications"
    echo "✅ Using command: $final_command"
    ;;
  3)
    echo "❌ Command approval cancelled. Exiting skill."
    exit 1
    ;;
  *)
    echo "❌ Invalid choice. Please enter 1, 2, or 3."
    exit 1
    ;;
esac

# Step 5: Update config with approved command
command_hash=$(echo -n "$final_command" | sha256sum | awk '{print $1}')

# Update metadata
sed -i "s/dev_command_approved: false/dev_command_approved: true/" .claude/performance-config.md
sed -i "s/dev_command_hash: null/dev_command_hash: \"$command_hash\"/" .claude/performance-config.md

echo "✅ Dev command approved and saved to configuration"

# Step 6: Start application and verify with retry logic
echo ""
echo "ℹ️ Starting application: $final_command"
echo "⏳ Waiting for application to respond on port $port..."

# Start in background
$final_command &
app_pid=$!

# Verify with curl retry loop
max_retries=30
retry_delay=2

for i in $(seq 1 $max_retries); do
  if curl -s http://localhost:$port >/dev/null 2>&1; then
    echo "✅ Application is running on port $port"
    break
  fi
  
  if [ $i -lt $max_retries ]; then
    echo "   Attempt $i/$max_retries - waiting ${retry_delay}s..."
    sleep $retry_delay
  else
    echo ""
    echo "❌ Application failed to start after $((max_retries * retry_delay)) seconds"
    echo "Please check application logs for errors."
    kill $app_pid 2>/dev/null
    exit 1
  fi
done
```

**Change Detection:**

Dev commands are hashed using SHA-256 to detect changes:
- If command unchanged and approved: Skip prompt
- If command changed: Re-prompt for approval
- If never approved: Prompt for approval

**Error Handling:**

- If auto-discovery fails: Prompt manual input
- If user denies approval: Stop execution with actionable message
- If port verification fails: Stop execution with instructions

**Configuration Updates:**

After approval, update `.claude/performance-config.md`:
1. Development Environment table: Dev Command, Documentation Source, Port, Last Validated
2. Metadata: `dev_command_approved: true`, `dev_command_hash: "{sha256}"`

---

## Pattern 8: Code Intelligence Strategy (Serena-First with Grep Fallback)

**Purpose:** Ensure robust code analysis by always trying Serena MCP tools first, with automatic Grep fallback

**When to use:** **MANDATORY** for ALL code analysis operations including:
- Symbol lookup (finding functions, classes, handlers)
- File search and discovery
- Schema extraction (struct/class definitions)
- Reference counting (finding callers)
- AST/semantic analysis
- Any source code inspection or parsing

**Used by:**
- performance-baseline (Step 3.0 probe; Steps 3.1-A/B, 3.1.1-A/B, 3.5-A/B)
- performance-analyze-module (Step 6.9 probe; Steps 7.1-A/B, 7.2-A/B, 7.3–7.6)
- performance-implement-optimization (any code inspection during implementation)
- Any future skills that inspect source code

**Core Principle:**

```
GATE: One live Serena probe call at skill start sets serena_mode for the entire run.
  serena_mode = live           → Follow Path A steps (Serena-only, no grep)
  serena_mode = down           → Follow Path B steps (Grep, Serena probe errored)
  serena_mode = not-configured → Follow Path B steps (no Serena instance in config)
```

**Procedure:**

### Step 1: Live Serena Probe

Read `serena_instance` from the skill's config source (`performance-config.md` or `CLAUDE.md`):

```bash
serena_instance=$(grep "Serena Instance" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
```

**If `serena_instance` is non-empty and not "—":**

Call `mcp__{serena_instance}__get_symbols_overview` with `relative_path="."`.

- **Response received (any result, including empty list):** `serena_mode = live`. Store the overview result for use in subsequent steps.
- **Error response received:** `serena_mode = down`. Record exact error string.

**If `serena_instance` is "—" or empty:** `serena_mode = not-configured`.

> The probe call doubles as useful data — the overview of the project root is the starting map
> for symbol discovery. Store and reuse it; do not discard it.

---

### Step 2-A: Code Analysis — Serena Path (`serena_mode = live`)

> **Grep and shell-based symbol discovery are not available in this path.**
> If an individual tool call errors on a specific file, mark that file
> `analysis_status: error` and continue with remaining files. Do not switch to grep.

Use the appropriate Serena tool for each operation:

| Operation | Tool | Key Parameters |
|---|---|---|
| All functions in a file | `find_symbol` | `name_path_pattern="/"`, `include_body=true`, `include_kinds=[12]`, `max_matches=100` |
| Callers of a function | `find_referencing_symbols` | `name_path=handler_name`, `relative_path=file` |
| File/module overview | `get_symbols_overview` | `relative_path=file`, `depth=1` |
| Named symbol search | `find_symbol` | `name_path_pattern=name`, `substring_matching=true` |
| Trace call to declaration | `find_declaration` | `relative_path=file`, `regex="obj\\.(method)\\("`, `include_body=true` |
| Find trait implementations | `find_implementations` | `name_path="Trait/method"`, `relative_path=file`, `include_info=true` |

**Batch over HTTP methods:** A single `find_symbol` call per file with `name_path_pattern="/"`
and `include_body=true` returns all handler functions including their route decorators
(`#[get]`, `#[post]`, etc.). Do not make separate calls per HTTP method.

Set `discovery_method = "Serena MCP"` and `confidence = "high"` on all results.

---

### Step 2-B: Code Analysis — Grep Path (`serena_mode = down | not-configured`)

> This path is followed only when Step 1 recorded `serena_mode = down` or `not-configured`.
> Document the reason in generated reports.

Use Grep and Read tools for symbol discovery. Apply framework-specific patterns defined in
each skill's discovery step.

Set `discovery_method = "Grep"` and `confidence = "medium"` on all results.

### Step 3: Document Method in Reports

Always document which analysis method was used in generated reports:
- Include "Analysis Method: Serena MCP (High Confidence)" or "Analysis Method: Grep (Fallback - Medium Confidence)"
- Add confidence level to anti-pattern detection tables
- If using Grep fallback, include limitations note

### Step 4: Confidence Levels

**High Confidence (Serena MCP):**
- Full AST/semantic analysis
- Accurate symbol resolution
- Cross-file reference tracking
- Type-aware field extraction
- Control flow analysis

**Medium Confidence (Grep - Good Patterns):**
- Pattern matching with context window
- Literal string search
- Line-proximity heuristics
- Best-effort parsing

**Low Confidence (Grep - Limitations):**
- Cannot detect destructuring (`const { field } = data`)
- Cannot track dynamic property access (`data[key]`)
- Cannot analyze control flow across functions
- May miss patterns split across many lines
- False positives on pattern matches in comments/strings

### Step 5: Error Handling Matrix

| `serena_mode` | Individual call result | Action | Confidence |
|---|---|---|---|
| `live` | Call succeeds | Use result, continue in Path A | High |
| `live` | Call errors on specific file | Mark file `analysis_status: error`, continue in Path A | High (partial) |
| `down` | — | Use Path B (Grep) throughout | Medium |
| `not-configured` | — | Use Path B (Grep) throughout | Medium |
| `live` + all files errored | All calls errored | Document in report as "Not Analyzed" | N/A |

---

## Pattern 9: Config Write Protection

**Purpose:** Prevent concurrent writes to `performance-config.md` from two simultaneous skill
executions (e.g., two developers running baseline at the same time on the same machine, or a CI
run overlapping a local run).

**When to use:** Immediately before writing `performance-config.md` in any skill that modifies it.

**Used by:**
- performance-setup (Step 7 — write config)
- performance-baseline (Step 3.10 — workflow update; Step 9.6 — baseline metadata update)
- performance-implement-optimization (Step 9.5 — result report; if config updated)

**Mechanism:** Optimistic lockfile using a sentinel file. Because skills are executed by an AI
agent using file-read and file-write tool calls (not a continuous bash process), POSIX `flock` is
ineffective. Instead, use a repo-scoped sentinel file and mtime-based change detection.

**Procedure:**

### Step A – Acquire lock

1. Determine the lock file path (scoped to the repository to avoid cross-project conflicts):
   ```
   lock_file = "{target-repo-path}/.claude/performance-config.lock"
   ```

2. Check whether the lock file exists:
   - If it exists, read its contents (should contain `{skill-name} {ISO-timestamp} {pid}`).
   - If the lock is older than **5 minutes**, consider it stale and proceed (previous skill likely crashed).
   - If the lock is fresh (< 5 minutes old), inform the user:
     > ⚠️ **Config file locked**
     >
     > Another performance skill appears to be running:
     > `{lock-file-contents}`
     >
     > If no other skill is running, delete the lock file and retry:
     > ```
     > rm {target-repo-path}/.claude/performance-config.lock
     > ```
     >
     > Waiting 30 seconds before retrying…
   - Wait 30 seconds and re-check once. If still locked, stop execution.

3. Create the lock file with:
   ```
   {skill-name} {ISO-8601-timestamp} {random 6-digit token}
   ```
   Write the lock file before reading or modifying the config.

### Step B – Read config, record mtime

Read `performance-config.md` and note its last-modified timestamp (using `git log -1 --format="%ai" -- .claude/performance-config.md` or file stat).

### Step C – Modify config

Apply the intended changes to the in-memory config content.

### Step D – Verify config unchanged before writing

Before writing, re-read the file's current last-modified timestamp.

If the timestamp has changed since Step B, another process has written the file concurrently:
> ⚠️ **Config was modified by another process between read and write.**
>
> Please re-run this skill to pick up the latest configuration.

Delete the lock file and stop execution.

If unchanged, write the updated config.

### Step E – Release lock

Delete the lock file:
```
rm {target-repo-path}/.claude/performance-config.lock
```

Always release the lock — even if the write fails. Failing to release leaves the repo in a
locked state until the 5-minute stale timeout.

**Error handling:**

- If the write itself fails (permissions, disk full), delete the lock file, inform user, and stop.
- If the skill is interrupted before Step E, the lock will expire automatically after 5 minutes.

**Note:** This pattern protects against the most common concurrency scenario (two developers
starting baseline at the same time). It does not prevent all races — a very short window between
Step D's check and the write remains. For production CI environments, prefer serialising
performance skill runs at the pipeline level.

---

## Pattern 10: API Profiling

**Purpose:** Execute accurate HTTP benchmarking of backend API endpoints using a curl-loop percentile calculator, with cache effectiveness measurement.

**When to use:**
- Backend-only baseline capture (api-benchmark mode)
- Module-level dynamic performance testing
- Any scenario requiring accurate API latency percentiles (p50, p95, p99)

**Used by:**
- performance-baseline (Step 9.A — API Benchmark Mode for backend-only)
- performance-analyze-module (Step 7.7 — Dynamic Performance Testing)

**Prerequisites:**

**For all callers:**
- Backend service must be running on localhost
- `curl` command must be available (for HTTP requests and timing)
- `bc` command must be available (for cache improvement calculation)

**For performance-analyze-module only:**
- Test data manifest must exist at `.claude/performance/test-data/manifest.json`

**For performance-baseline:**
- Test data manifest is created by baseline itself (no prerequisite)
- Working endpoints identified in Step 8.4.B9 verification

**Dependencies:**
- `curl` (HTTP requests and timing via `-w '%{time_total}'`)
- `bc` (cache improvement percentage calculation)

---

### Step A – Check Prerequisites

```bash
# Check if backend running
port=$(grep "| Port |" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)

if ! timeout 2 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
  echo "ℹ️ Backend not running. Skipping dynamic testing."
  skip_dynamic=true
  return
fi

# For performance-analyze-module: Check if test data manifest exists
# (performance-baseline creates the manifest, so this check is skipped there)
if [ "$CALLER_SKILL" = "performance-analyze-module" ]; then
  if [ ! -f ".claude/performance/test-data/manifest.json" ]; then
    echo "⚠️ Test data manifest not found."
    echo "   Run /sdlc-workflow:performance-baseline first to discover test data."
    skip_dynamic=true
    return
  fi
fi

# Verify curl is available
if ! command -v curl &>/dev/null; then
  echo "❌ curl not found. Cannot run dynamic API profiling."
  skip_dynamic=true
  return
fi

echo "ℹ️ curl found — proceeding with curl-loop API profiling"
```

**Error handling:**
- Backend not running → Skip dynamic profiling, continue with static analysis only
- curl unavailable → Skip dynamic profiling with clear error message

**Note:** Error paths use `return` to exit early. Callers must invoke Pattern 10 logic inside a shell function context for `return` to work correctly. Example:
```bash
function run_api_profiling() {
  # Apply Pattern 10 here
  # return statements will exit this function, not the entire script
}
run_api_profiling
```

---

### Step B – Execute Benchmark with Cache Measurement

**Methodology:**
1. **Cold cache (first request):** Single `curl` request measures worst-case latency
2. **Warm cache (aggregate stats):** `iterations` curl requests collected into an array; p50/p95/p99 derived by sorting

**Implementation:**

```bash
# Read test configuration
iterations=$(grep "| Iterations |" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)

# Declare associative array outside loop
declare -A dynamic_results

# Use process substitution to avoid subshell scope loss
while IFS='|' read -r scenario_name test_url; do
  # Initialize cache_status for this iteration
  cache_status=""

  url="http://localhost:${port}${test_url}"

  echo "Testing: $scenario_name ($url)"

  # 1. First request (cache miss) - measures cold-cache worst-case latency
  first_request_ms=$(curl -o /dev/null -s -w '%{time_total}\n' "$url" | \
    awk '{printf "%.0f", $1 * 1000}')

  if [ -z "$first_request_ms" ]; then
    echo "  ⚠️ First request failed"
    continue
  fi

  # 2. Subsequent requests (cache warm) - curl loop for percentile calculation
  times=()
  for i in $(seq 1 "$iterations"); do
    t=$(curl -o /dev/null -s -w '%{time_total}' "$url" | awk '{printf "%.0f", $1 * 1000}')
    [ -n "$t" ] && times+=("$t")
  done

  if [ "${#times[@]}" -eq 0 ]; then
    echo "  ⚠️ All warm-cache requests failed"
    continue
  fi

  # Sort times and compute percentiles via array index
  sorted=($(printf '%s\n' "${times[@]}" | sort -n))
  n=${#sorted[@]}
  p50=${sorted[$((n * 50 / 100))]}
  p95=${sorted[$((n * 95 / 100))]}
  p99=${sorted[$((n * 99 / 100))]}
  mean=$(printf '%s\n' "${times[@]}" | awk '{s+=$1} END {printf "%.0f", s/NR}')

  # Validate output
  if [ -z "$p95" ] || [ "$p95" = "0" ]; then
    echo "  ⚠️ Failed to produce valid percentile stats"
    continue
  fi

  # Cache effectiveness: first request vs subsequent mean
  # Guard against division by zero
  if [ -z "$first_request_ms" ] || [ "$first_request_ms" -eq 0 ]; then
    cache_status="N/A"
    cache_improvement="0"
  else
    cache_improvement=$(echo "scale=2; ($first_request_ms - $mean) / $first_request_ms * 100" | bc)
  fi

  # Classify cache effectiveness (only if not already N/A)
  if [ "$cache_status" != "N/A" ]; then
    if (( $(echo "$cache_improvement > 50" | bc -l) )); then
      cache_status="Effective"
    elif (( $(echo "$cache_improvement > 20" | bc -l) )); then
      cache_status="Moderate"
    else
      cache_status="Minimal"
    fi
  fi

  # Save results
  dynamic_results["$scenario_name"]=$(cat <<JSON
{
  "test_url": "$test_url",
  "iterations": $iterations,
  "p50_ms": "$p50",
  "p95_ms": "$p95",
  "p99_ms": "$p99",
  "mean_ms": "$mean",
  "first_request_ms": $first_request_ms,
  "subsequent_mean_ms": "$mean",
  "cache_improvement_pct": "$cache_improvement",
  "cache_status": "$cache_status"
}
JSON
)

  echo "  ✓ p50: ${p50}ms, p95: ${p95}ms, Cache: ${cache_improvement}% ($cache_status)"

done < <(jq -r '.endpoints | to_entries[] | "\(.key)|\(.value.test_url)"' \
  .claude/performance/test-data/manifest.json)

# Save results to file (for cross-skill persistence)
declare -p dynamic_results > .claude/performance/test-data/dynamic-results.sh
```

**Percentile calculation:**
- Runs `iterations` sequential curl requests and collects response times into a bash array
- Sorts the array numerically and selects values at the 50th, 95th, and 99th index positions
- Mean is computed as the arithmetic average across all collected times

---

### Step C – Cache Effectiveness Classification

**Formula:**
```
cache_improvement = (cold_latency - warm_mean) / cold_latency × 100%
```

**Classification thresholds:**
- **Effective:** > 50% improvement (cache working well)
- **Moderate:** 20-50% improvement (some caching benefit)
- **Minimal:** < 20% improvement (cache ineffective or not used)
- **N/A:** First request failed or zero latency

**Example:**
- Cold: 1180ms
- Warm: 147ms
- Improvement: (1180 - 147) / 1180 × 100 = 87.5% → "Effective"

---

### Step D – Result Storage

**Result format (per endpoint):**
```json
{
  "test_url": "/api/v2/analysis/component",
  "iterations": 10,
  "p50_ms": "140",
  "p95_ms": "178",
  "p99_ms": "180",
  "mean_ms": "147",
  "first_request_ms": 1180,
  "subsequent_mean_ms": "147",
  "cache_improvement_pct": "87.54",
  "cache_status": "Effective"
}
```

**Storage mechanism:**
- **Associative array** (in-skill usage):
  ```bash
  declare -A dynamic_results
  dynamic_results["$scenario_name"]="<json>"
  ```
- **Persisted file** (cross-skill sharing):
  ```bash
  declare -p dynamic_results > .claude/performance/test-data/dynamic-results.sh
  ```

**Reading results in subsequent steps:**
```bash
# Source the persisted results
source .claude/performance/test-data/dynamic-results.sh

# Extract metrics for a specific scenario
result_json="${dynamic_results[$scenario_name]}"
p95=$(echo "$result_json" | jq -r '.p95_ms')
cache_status=$(echo "$result_json" | jq -r '.cache_status')
```

---

### Error Handling

**Service unavailable:**
```bash
if ! timeout 2 bash -c "</dev/tcp/localhost/$port" 2>/dev/null; then
  echo "ℹ️ Backend not running. Skipping dynamic testing."
  skip_dynamic=true
  return
fi
```

**Per-endpoint failures:**
```bash
if [ -z "$first_request_ms" ]; then
  echo "  ⚠️ First request failed"
  continue  # Skip this endpoint, continue with next
fi

if [ -z "$p95" ] || [ "$p95" = "0" ]; then
  echo "  ⚠️ Failed to produce valid percentile stats"
  continue
fi
```

**Graceful degradation:**
- Missing test data → Skip profiling, show instructions to run baseline first
- Individual endpoint failure → Log warning, continue with remaining endpoints
- Authentication errors → Note in report, suggest `AUTH_DISABLED=true`

---

## Pattern 11: Jira Access Strategy

**Purpose:** Unified strategy for attempting Jira operations with MCP-first approach and REST API fallback

**When to use:** Before any Jira operation (issue creation, updates, transitions, comments)

**Used by:**
- performance-plan-optimization (Steps 8-10)
- performance-implement-optimization (Steps 2-4, 11-12)
- performance-verify-optimization (Steps 1, 4, 17-18)

**Procedure:**

**Step 1: Determine plugin root directory (do this once at skill initialization)**

**Apply:** [Pattern 0: Plugin Root Resolution](#pattern-0-plugin-root-resolution)

This resolves `$plugin_root` to the installed plugin directory (e.g., `~/.claude/plugins/cache/sdlc-plugins-local/sdlc-workflow/0.6.1/`)

**Step 2: For every Jira operation:**

1. **Attempt MCP first** (preferred method using Atlassian MCP server)
2. **If MCP fails, prompt user:**
   ```
   ❌ Atlassian MCP failed: {error_message}
   
   Would you like to use Jira REST API v3 fallback?
   
   Options:
   1. Yes - Use REST API (requires credentials)
   2. No - Skip this Jira operation
   3. Retry - I'll fix MCP configuration and retry
   
   Choose (1/2/3):
   ```

3. **If "1. Yes":** Check CLAUDE.md for existing REST API credentials, collect if missing, then use Python client
4. **If "2. No":** Skip the Jira operation and inform user
5. **If "3. Retry":** Retry MCP once

**REST API Equivalents:**

Common Jira operations with REST API fallback commands (using $plugin_root from Step 1):

- **Get issue:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" get_issue <id> --fields "*all"
  ```

- **Get user info:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" get_user_info
  ```

- **Assign issue:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" update_issue <id> --fields-json '{"assignee": {"id": "<accountId>"}}'
  ```

- **Transition issue:** 
  ```bash
  # First get transitions
  python3 "$plugin_root/scripts/jira-client.py" get_transitions <id>
  # Then transition (find ID for target status from above)
  python3 "$plugin_root/scripts/jira-client.py" transition_issue <id> --transition-id <id>
  ```

- **Update fields:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" update_issue <id> --fields-json '<json>'
  ```

- **Add comment:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" add_comment <id> --comment-md "<text>"
  ```

- **Create issue:** 
  ```bash
  python3 "$plugin_root/scripts/jira-client.py" create_issue --project <key> --issue-type <id> --summary "<text>" --description-md "<text>"
  ```

**Error handling:**

- If REST API also fails, report error and stop
- Always inform user which method was used (MCP or REST API)
- For missing credentials, prompt once and store in session for reuse

**Important:**

- REST API requires: `JIRA_SERVER_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` environment variables
- `$plugin_root` variable must be determined once at skill initialization (Step 1) and reused for all Jira operations
- The plugin path is typically `~/.claude/plugins/sdlc-workflow` but may vary by installation
- REST API fallback is only for Jira operations - never for code analysis or file operations

---

## Pattern 12: Call Chain Analysis Strategy

**Purpose:** Recursively trace function calls from an entry point (HTTP handler, service method, etc.) to detect performance anti-patterns hidden at any depth in the call graph — including service-layer N+1 queries, wasted computation, and unnecessary database operations.

**When to use:** After reading a handler/entry-point body, when the handler delegates to service methods, model builders, or utility functions that may contain queries, loops, or expensive operations.

**Used by:**
- performance-analyze-module (Steps 7.6.2-A, 7.6.2-B)
- Any future skills that need deep code inspection

**Core Principle:**

The pattern maintains three data structures during traversal:

1. **`call_graph`** — ordered list of `{caller, callee, file, depth}` edges representing the call tree
2. **`visited`** — set of `(file, symbol_name)` pairs to prevent infinite recursion on circular calls
3. **`query_ledger`** — list of `{description, depth, loop_multiplier, source_file, source_symbol}` entries for total query counting

**Configurable depth:** `analysis_chain_depth` (default: 3, read from Analysis Assumptions in `performance-config.md`).

---

### Step 1: Extract Call Sites from Body

Given a function body (from `find_symbol` with `include_body=true` or from the Read tool), extract method/function calls by matching these patterns:

| Call Pattern | Example | Resolution Strategy |
|---|---|---|
| `self.method_name(...)` | `self.fetch_sbom(id, &tx)` | Resolve within current impl block |
| `service.method_name(...)` | `fetcher.fetch_sbom_details(...)` | Determine service type from params, resolve in service file |
| `Type::associated_fn(...)` | `SbomDetails::from_entity(...)` | Resolve in type's impl block |
| `module::function(...)` | `utils::parse_id(...)` | Resolve in module directory |
| Direct function call | `decompress_async(bytes, ...)` | Resolve in current module or imports |

**Priority for tracing:** Focus on calls that are likely to contain database queries or expensive operations. Deprioritize calls to standard library functions, logging, serialization, or simple utility functions.

**Model builder heuristic:** Calls matching `Type::from_entity(...)`, `Type::from_row(...)`, `Type::from_model(...)`, or `Type::new(...)` are high-priority — these commonly contain hidden queries in Rust/Java/Python ORMs.

---

### Step 2: Resolve Each Call Site

**Path A — Serena (`serena_mode = live`):**

| Call Type | Serena Tool | Parameters |
|---|---|---|
| `self.method(...)` in same file | `find_declaration` | `relative_path=current_file`, `regex="self\\.(method)\\("`, `include_body=true` |
| `service.method(...)` typed param | `find_symbol` | `name_path_pattern="ServiceType/method"`, `relative_path=service_dir/`, `include_body=true`, `max_matches=1` |
| `Type::associated_fn(...)` | `find_symbol` | `name_path_pattern="Type/associated_fn"`, `include_body=true`, `max_matches=1` |
| Trait method call | `find_implementations` | `name_path="TraitName/method"`, `relative_path=file`, `include_info=true` |

If `find_symbol` returns no results, retry once with `substring_matching=true`. If still no result, record "Unresolved call: {call_expression}" and skip this branch.

**Path B — Grep (`serena_mode = down | not-configured`):**

1. Determine the target type from handler parameters (e.g., `fetcher: web::Data<SbomService>`)
2. Find the impl block: `grep -rn "impl ServiceType" modules/ --include="*.rs"`
3. Find the method: `grep -n "fn method_name" path/to/service.rs`
4. Read the method body with the Read tool (use line offset/limit from grep result)

Set `confidence = "medium"` at depth 0, `"low"` at depth > 1 for all Grep-path findings.

---

### Step 3: Recurse with Depth Limit and Cycle Detection

Before descending into a callee:

1. **Check depth:** `depth < analysis_chain_depth` (default 3)
2. **Check cycles:** `(callee_file, callee_name) not in visited`

**If either check fails:**
- Record the call edge in `call_graph` with annotation: `"⋯ Depth limit"` or `"⟳ Circular"`
- Do NOT descend — continue with remaining call sites at current depth

**If both checks pass:**
1. Add `(callee_file, callee_name)` to `visited`
2. Read the callee's body (Serena `find_symbol` with `include_body=true`, or Read tool)
3. Apply anti-pattern detection (Step 4)
4. Extract call sites from this callee's body → recurse back to Step 1 at `depth + 1`

---

### Step 4: Apply Anti-Pattern Checks at Each Depth

At every function body encountered during traversal, check for:

- **N+1 patterns:** Queries inside loops (same detection logic as Step 7.3 of performance-analyze-module)
- **Unused JOINs:** JOIN operations where joined table fields are never accessed (same as Step 7.6.1)
- **SELECT \* patterns:** ORM queries that fetch all columns without `.select_only()` (same as Step 7.6)
- **Missing caching:** Expensive operations without cache layer (same as Step 7.5)
- **Unnecessary computation:** Work done that is discarded by the caller (detected by comparing return type fields against caller's field access — see Step 7.6.3 in performance-analyze-module)
- **Conditional queries via lazy-load parameters (Memo/Option pattern):** When a function body
  contains a match/if on a `Memo<T>`, `Option<T>`, or similar lazy-load wrapper where one branch
  triggers a DB query and the other uses a pre-provided value:
  - Identify the parameter name and its type (e.g., `issuer: Memo<organization::Model>`)
  - Detect the branching pattern:
    ```
    Memo::Provided(value) => /* use value directly, no query */
    Memo::NotProvided => entity.find_related(...).one(tx).await?  // QUERY
    ```
  - Walk the `call_graph` upward to find ALL callers of this function
  - For each caller, check whether it passes the lazy variant (`Memo::NotProvided`, `None`) or the
    pre-loaded variant (`Memo::Provided(...)`, `Some(...)`)
  - If a caller passes the lazy variant, add the conditional query to `query_ledger` with
    `conditional: true` and `trigger` annotation (see format below)
  - Multiply by the caller's loop context if the caller is itself inside a loop
  - **Language-specific patterns:**
    - **Rust:** `Memo::NotProvided`, `Option::None`, `Lazy::new(|| ...)`
    - **Java:** `Optional.empty()`, `null` parameter, `@Lazy` annotation
    - **Python:** `None` default parameter, `lazy=True` flag
    - **Node:** `undefined` / `null` parameter, callback-based lazy loading

For each query or expensive operation found, add an entry to `query_ledger`:
```
{
  description: "human-readable query description",
  source_file: "relative/path/to/file.rs",
  source_line: 123,
  source_symbol: "SbomSummary::from_entity",
  depth: 2,
  query_type: "SELECT" | "COUNT" | "INSERT" | "UPDATE" | "DELETE",
  conditional: false,
  trigger: null,
  loop_context: {
    in_loop: true/false,
    loop_variable: "items",
    estimated_iterations: 25 or "N",
    loop_source: "paginated query with default limit 25"
  }
}
```

For conditional queries (Memo/Option pattern), set:
```
  conditional: true,
  trigger: "Memo::NotProvided passed by {caller_name} at {file}:{line}"
```

---

### Step 5: Calculate Query Totals

After traversal completes, process `query_ledger` to compute effective query counts:

```
For each query Q in query_ledger:
    effective_multiplier = 1
    
    Walk the call_graph from handler root to Q's source_symbol.
    For each edge on the path:
        If the caller contains a loop that iterates over the callee:
            effective_multiplier *= loop_iteration_count
    
    Also check Q's own loop_context:
    If Q.loop_context.in_loop:
        effective_multiplier *= Q.loop_context.estimated_iterations
    
    Q.effective_count = effective_multiplier

total_queries = sum(Q.effective_count for all Q in query_ledger)
estimated_db_latency = total_queries * analysis_db_latency_ms  # from Analysis Assumptions in performance-config.md, default 10ms
```

**Loop iteration estimation heuristics:**
- Collection from paginated query: use page_size (typically 20-25)
- Collection from unbounded query: use "N" and flag as "missing pagination"
- Fixed-size input (enum, config): use exact count
- Indeterminate: use "N" with note

**Post-traversal analysis:** After query totals are computed, the completed `query_ledger` can be
analyzed for inter-query duplication — see
[Step 7.6.5 in performance-analyze-module](../performance-analyze-module/SKILL.md#step-765--inter-query-duplication-detection)
for detection of shared CTEs and overlapping SQL logic across queries within the same handler chain.

---

### Error Handling

| Error | Action |
|---|---|
| `find_declaration` fails for a call site | Log it, skip that branch, continue with others |
| `find_symbol` returns no results | Retry once with `substring_matching=true`; if still empty, skip branch |
| Function body too large (> 500 lines) | Read body but limit recursion: extract only top-10 call sites by priority |
| Circular call detected | Record edge with "⟳ Circular" annotation, do not descend |
| Depth limit reached | Record edge with "⋯ Depth limit" annotation, do not descend |

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
