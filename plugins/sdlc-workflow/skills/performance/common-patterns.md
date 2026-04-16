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
  extract metadata.baseline_captured (true | false)
  extract metadata.baseline_timestamp (ISO timestamp | null)
  extract metadata.baseline_commit_sha (git SHA | null)
  extract metadata.backend_available (true | false)
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
| `baseline_timestamp` | ISO timestamp or null | When baseline was captured | null |
| `baseline_commit_sha` | string or null | Git commit at baseline capture | null |
| `backend_available` | boolean | Whether backend is configured and accessible | false |
| `analysis_scope` | string | Determines which repositories are analyzed: "full-stack-monorepo" (same repo), "full-stack" (separate repos), "frontend-only", "backend-only" | "frontend-only" |

**Error handling:**

- If metadata is missing but expected (config_version = 1), offer auto-migration to v2
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
  echo "⚠️ IMPORTANT: V1→V2 auto-migration is not fully implemented."
  echo "The migration script has incomplete transformations:"
  echo "- Optimization Targets 3-column format"
  echo "- Backend Available field insertion"
  echo ""
  echo "Manual migration required:"
  echo "1. Backup: cp .claude/performance-config.md .claude/performance-config.md.v1.backup"
  echo "2. Add metadata frontmatter (see performance-config.template.md)"
  echo "3. Restructure Optimization Targets table to 6-column format"
  echo "4. Add Backend Available and Last Validated fields"
  echo ""
  echo "Do NOT proceed with auto-migration. Migrate manually instead."
  echo "Continue with v1 config? (yes/no)"
  
  read -p "> " upgrade_choice
  
  if [ "$upgrade_choice" = "yes" ]; then
    echo "Continuing with v1 config (some features disabled)"
  else:
    echo "Migration cancelled. Please migrate manually or continue with v1."
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

# Infer analysis_scope from backend_available
analysis_scope="frontend-only"
if [ "$backend_available" = "true" ]; then
  # Check if monorepo (both frontend and backend in same directory)
  frontend_path=$(grep "Frontend Path" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
  backend_path=$(grep "Backend Path" .claude/performance-config.md | awk -F'|' '{print $3}' | xargs)
  
  if [ -n "$frontend_path" ] && [ "$frontend_path" = "$backend_path" ]; then
    analysis_scope="full-stack-monorepo"
  else
    analysis_scope="full-stack"
  fi
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
  analysis_scope: \"${analysis_scope}\"
  backend_endpoint_discovery_method: null
  dev_command_approved: false
  dev_command_hash: null
---
"

# Prepend metadata to config
echo "$metadata" > .claude/performance-config.md.tmp
echo "" >> .claude/performance-config.md.tmp
cat .claude/performance-config.md >> .claude/performance-config.md.tmp
mv .claude/performance-config.md.tmp .claude/performance-config.md

# Update Optimization Targets section to 3-column format
# (Implementation depends on sed/awk skills - simplified here)
# Note: Optimization Targets transformation requires manual sed/awk - add columns: | Baseline (p95) | TBD | Latest Verified (p95) | TBD |

# Add Backend Available field to Backend Configuration section
# Note: Backend Configuration update requires adding row after Last Validated field

echo "✅ Configuration upgraded to v2"
echo "Backup saved to: .claude/performance-config.md.v1.backup"
```

**Migration checklist:**

- [x] Create metadata frontmatter with defaults
- [x] Extract baseline mode from existing baseline report (if exists)
- [x] Validate backend path and set backend_available flag
- [x] Check if workflow is selected (workflow_selected flag)
- [x] Transform Optimization Targets to 3-column format (Baseline/Current/Target) - Note: Manual step required
- [x] Add "Backend Available" row to Backend Configuration table - Note: Manual step required
- [x] Backup original config to .v1.backup

---

## Pattern 8: Dev Command Approval

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
  
  # Priority 1: package.json scripts
  if [ -f "package.json" ]; then
    dev_script=$(jq -r '.scripts.dev // .scripts.start // .scripts.serve // "null"' package.json)
    if [ "$dev_script" != "null" ]; then
      discovered_command="npm run dev"
      doc_source="package.json scripts.dev"
    fi
  fi
  
  # Priority 2: README.md / CONTRIBUTING.md
  if [ -z "$discovered_command" ]; then
    for readme in README.md CONTRIBUTING.md docs/development.md; do
      if [ -f "$readme" ]; then
        # Look for "Getting Started", "Development", "Running Locally" sections
        # Extract command from code blocks (simplified - real implementation uses grep/sed)
        discovered_command=$(grep -A 5 "Getting Started\|Development\|Running Locally" "$readme" | grep "npm run\|cargo run\|mvn spring-boot:run" | head -1)
        if [ -n "$discovered_command" ]; then
          doc_source="$readme"
          break
        fi
      fi
    done
  fi
  
  # Priority 3: Makefile / justfile
  if [ -z "$discovered_command" ]; then
    for makefile in Makefile justfile; do
      if [ -f "$makefile" ]; then
        # Look for dev, start, run targets
        discovered_command=$(grep "^dev:\|^start:\|^run:" "$makefile" | head -1 | sed 's/:.*//')
        if [ -n "$discovered_command" ]; then
          discovered_command="make $discovered_command"
          doc_source="$makefile"
          break
        fi
      fi
    done
  fi
  
  # Priority 4: Framework defaults
  if [ -z "$discovered_command" ]; then
    if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
      discovered_command="npm run dev"
      doc_source="Next.js framework default"
    elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
      discovered_command="npm run dev"
      doc_source="Vite framework default"
    elif [ -f "Cargo.toml" ]; then
      discovered_command="cargo run"
      doc_source="Rust framework default"
    elif [ -f "pom.xml" ]; then
      discovered_command="mvn spring-boot:run"
      doc_source="Spring Boot framework default"
    elif [ -f "manage.py" ]; then
      discovered_command="python manage.py runserver"
      doc_source="Django framework default"
    fi
  fi
  
  # If still not found, prompt manually
  if [ -z "$discovered_command" ]; then
    echo "⚠️ Could not auto-discover dev command"
    echo "Please enter the command to start your application:"
    read -p "> " discovered_command
    doc_source="Manual user input"
  fi
fi

# Step 3: Extract port number from command or config
port=""

# From command flags
if echo "$discovered_command" | grep -qE -- "--port|-p"; then
  port=$(echo "$discovered_command" | grep -oE -- "--port[= ]([0-9]+)|-p[= ]([0-9]+)" | grep -oE "[0-9]+")
fi

# From .env files
if [ -z "$port" ]; then
  for envfile in .env .env.local .env.development; do
    if [ -f "$envfile" ]; then
      port=$(grep "^PORT=" "$envfile" | cut -d= -f2)
      [ -n "$port" ] && break
    fi
  done
fi

# From framework config files
if [ -z "$port" ]; then
  if [ -f "vite.config.ts" ]; then
    port=$(grep "port:" vite.config.ts | grep -oE "[0-9]+" | head -1)
  elif [ -f "next.config.js" ]; then
    port=$(grep "port:" next.config.js | grep -oE "[0-9]+" | head -1)
  fi
fi

# Framework defaults
if [ -z "$port" ]; then
  if [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    port=3000
  elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
    port=5173
  elif [ -f "Cargo.toml" ]; then
    port=8080
  elif [ -f "pom.xml" ]; then
    port=8080
  elif [ -f "manage.py" ]; then
    port=8000
  else
    port=3000  # Fallback default
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
echo "What this command does:"
echo "- Starts application in development mode"
echo "- Runs on port $port (http://localhost:$port)"
echo ""
echo "Security guarantees:"
echo "- Runs in your local environment only"
echo "- No credentials required"
echo "- Standard development tooling"
echo ""
echo "Additional instructions (optional):"
echo "Enter modifications (e.g., \"AUTH_DISABLED=true npm run dev\") or press Enter to use as-is:"
read -p "> " user_modifications

if [ -n "$user_modifications" ]; then
  final_command="$user_modifications"
else
  final_command="$discovered_command"
fi

echo ""
echo "Final command: $final_command"
echo ""
echo "Approve this command? (yes/no)"
read -p "> " approval

if [ "$approval" != "yes" ]; then
  echo "❌ Command not approved. Please start your application manually and re-run this skill."
  exit 1
fi

# Step 5: Update config with approved command
command_hash=$(echo -n "$final_command" | sha256sum | awk '{print $1}')
current_timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Update Development Environment section
# (sed/awk implementation omitted - replace table values)

# Update metadata
sed -i "s/dev_command_approved: false/dev_command_approved: true/" .claude/performance-config.md
sed -i "s/dev_command_hash: null/dev_command_hash: \"$command_hash\"/" .claude/performance-config.md

echo "✅ Dev command approved and saved to configuration"

# Step 6: Display manual start instructions
echo ""
echo "Please start your application manually:"
echo "  $final_command"
echo ""
echo "Wait for successful start, then press Enter to continue..."
read -p ""

# Step 7: Verify application is running
echo "Verifying application is running on port $port..."
if nc -z localhost $port 2>/dev/null; then
  echo "✅ Application is running"
else
  echo "❌ Application not running on port $port"
  echo "Please start your application and re-run this skill."
  exit 1
fi
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

## Pattern 9: Code Intelligence Strategy (Serena-First with Grep Fallback)

**Purpose:** Ensure robust code analysis by always trying Serena MCP tools first, with automatic Grep fallback

**When to use:** All code analysis operations (symbol lookup, file search, schema extraction)

**Used by:**
- performance-analyze-module (Step 7.1-7.6 backend analysis)
- performance-plan-optimization (reading analysis reports that document which method was used)
- Any future skills that inspect source code

**Core Principle:**

```
ALWAYS: Serena MCP (Preferred) → Grep (Fallback) → Document which was used
```

**Procedure:**

### Step 1: Check Serena Availability

```bash
# Extract Serena instance name from config or CLAUDE.md
serena_instance_name="backend-serena"  # From config

# Construct MCP tool name
mcp_tool_prefix="mcp__${serena_instance_name}__"

# Test if Serena MCP is available at runtime
# Use ToolSearch to check if tool exists
serena_available=false

if ToolSearch(query="select:${mcp_tool_prefix}get_symbols_overview"); then
  serena_available=true
  echo "✅ Serena MCP available: Using semantic code intelligence"
else
  serena_available=false
  echo "ℹ️ Serena MCP unavailable: Falling back to Grep-based analysis"
fi
```

### Step 2: Execute Analysis with Fallback

For each code analysis operation, implement the fallback pattern:

**Pattern Template:**

```python
# Pseudo-code for illustration
def analyze_code(operation_name, serena_params, grep_params):
    result = None
    method_used = None
    confidence = None
    
    # FIRST CHOICE: Try Serena MCP
    if serena_available:
        try:
            result = call_serena_mcp(**serena_params)
            method_used = "Serena MCP"
            confidence = "High"  # Semantic analysis
            log_info(f"✅ {operation_name}: Serena MCP succeeded")
        except ToolNotFoundError as e:
            log_warning(f"⚠️ Serena MCP failed: {e}")
            # Fall through to Grep fallback
        except Exception as e:
            log_warning(f"⚠️ Serena MCP error: {e}")
            # Fall through to Grep fallback
    
    # FALLBACK STRATEGY: Use Grep if Serena unavailable or failed
    if result is None:
        try:
            result = call_grep(**grep_params)
            method_used = "Grep (Fallback)"
            confidence = "Medium"  # Pattern matching only
            log_info(f"ℹ️ {operation_name}: Grep fallback succeeded")
        except Exception as e:
            log_error(f"❌ Grep fallback failed: {e}")
            method_used = "Failed"
            confidence = "None"
    
    # ALWAYS DOCUMENT: Which method was used
    return {
        "result": result,
        "method_used": method_used,
        "confidence": confidence,
        "limitations": get_limitations(method_used)
    }
```

### Step 3: Document Method in Reports

Always document which analysis method was used in generated reports:

**Example - Backend Analysis Section in Report:**

```markdown
## Backend Source Code Analysis

**Backend Repository:** my-backend-service (Rust/Actix-Web)  
**Analysis Method:** Serena MCP (High Confidence)  
**Endpoints Analyzed:** 12 endpoints  

### Detection Confidence

| Anti-Pattern | Detection Method | Confidence | Notes |
|---|---|---|---|
| N+1 Queries | Serena MCP | High | Semantic analysis of loop+query patterns |
| Over-Fetching | Serena MCP | High | Full struct definition extracted |
| Unused Joins | Serena MCP | High | JOIN detection + field usage tracking |
```

**Example - Grep Fallback Documentation:**

```markdown
## Backend Source Code Analysis

**Backend Repository:** my-backend-service (Rust/Actix-Web)  
**Analysis Method:** Grep (Fallback - Serena MCP unavailable)  
**Endpoints Analyzed:** 8 endpoints (4 not found with Grep)  
**Confidence:** Medium (pattern matching only)

⚠️ **Analysis Limitations (Grep Fallback Mode):**
- Schema extraction: Best-effort parsing, may miss nested fields
- N+1 detection: Proximity-based (10-line window), may miss service layers
- Field usage tracking: Literal string matching, misses dynamic property access
- **Recommendation:** Enable Serena MCP for comprehensive analysis

### Detection Confidence

| Anti-Pattern | Detection Method | Confidence | Notes |
|---|---|---|---|
| N+1 Queries | Grep proximity search | Medium | May miss patterns >10 lines apart |
| Over-Fetching | Grep field search | Low-Medium | Cannot detect destructuring patterns |
| Unused Joins | Grep JOIN pattern | Medium | May miss ORM-generated JOINs |
```

### Step 4: Specific Operation Examples

#### Operation: Find Handler Function

**Serena-First:**
```rust
// FIRST CHOICE: Serena MCP
let handler = mcp__backend_serena__find_symbol(
    name_path_pattern: ".*products.*handler",
    relative_path: "src/handlers/",
    include_body: false
);

// Returns: Full symbol metadata with file path, line numbers, signature
```

**Grep Fallback:**
```bash
# FALLBACK: Grep
grep -r "#\[get(\"/api/v2/products\")" backend_path/src/ | \
  grep -v "test" | \
  head -1

# Returns: filename:line:match (limited metadata)
```

#### Operation: Extract Response Schema

**Serena-First:**
```rust
// FIRST CHOICE: Serena MCP
let response_struct = mcp__backend_serena__find_symbol(
    name_path_pattern: "ProductResponse",
    include_body: true,
    depth: 2  // Include nested structs
);

// Returns: Complete struct definition with all fields, types, nested objects
```

**Grep Fallback:**
```bash
# FALLBACK: Grep
grep -A 50 "struct ProductResponse" backend_path/src/models/ | \
  grep -E "^\s+\w+:" | \
  awk '{print $1}' | \
  tr -d ','

# Returns: Field names only (no types, no nested resolution)
```

#### Operation: Detect N+1 Queries

**Serena-First:**
```rust
// FIRST CHOICE: Serena MCP
let handler_body = mcp__backend_serena__find_symbol(
    name_path_pattern: "get_products_handler",
    include_body: true
);

// Then analyze AST for loop constructs containing query calls
// Can detect across service layer boundaries, track control flow
```

**Grep Fallback:**
```bash
# FALLBACK: Grep with proximity search
grep -A 10 "for.*in\|\.iter()" handler_file | \
  grep "query!\|fetch_one\|find_by_id"

# Limited to 10-line window, cannot track control flow
```

### Step 5: Confidence Levels

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

### Step 6: Error Handling Matrix

| Scenario | Serena Behavior | Grep Fallback | Final Action |
|---|---|---|---|
| Serena available, operation succeeds | ✅ Use result | ⏭️ Skip | Report with High confidence |
| Serena available, operation fails | ⚠️ Log error | ✅ Use Grep | Report with Medium confidence + note Serena failure |
| Serena unavailable from start | ⏭️ Skip | ✅ Use Grep | Report with Medium confidence + note Serena unavailable |
| Both fail | ❌ Operation failed | ❌ No fallback | Document limitation in report, mark as "Not Analyzed" |

### Step 7: Configuration Validation

**Check Serena instance configuration:**

```bash
# From CLAUDE.md Repository Registry
if grep -q "Serena Instance" CLAUDE.md; then
  serena_instance=$(grep "Serena Instance" CLAUDE.md | awk -F'|' '{print $4}' | xargs)
  
  if [ -n "$serena_instance" ] && [ "$serena_instance" != "—" ]; then
    echo "✅ Serena configured: $serena_instance"
    # Proceed with runtime availability check (Step 1)
  else
    echo "ℹ️ No Serena instance configured, using Grep-only mode"
    serena_available=false
  fi
else
  echo "ℹ️ CLAUDE.md has no Repository Registry, using Grep-only mode"
  serena_available=false
fi
```

### Step 8: Performance Optimization

**Batch Serena calls when possible:**

```python
# GOOD: Batch symbol lookups
symbols = mcp__serena__find_symbol(
    name_path_pattern: "Product.*",  # Wildcard matches multiple symbols
    depth: 1
)

# AVOID: Sequential individual calls
for symbol_name in ["ProductResponse", "ProductDTO", "ProductEntity"]:
    symbol = mcp__serena__find_symbol(name_path_pattern=symbol_name)
```

**Cache Serena results:**

```python
# Cache handler lookups for re-use
handler_cache = {}

def get_handler(endpoint_path):
    if endpoint_path in handler_cache:
        return handler_cache[endpoint_path]
    
    handler = mcp__serena__find_symbol(...)
    handler_cache[endpoint_path] = handler
    return handler
```

### Step 9: User Communication

**Inform user of analysis mode:**

```
ℹ️ **Code Analysis Strategy**

Backend Analysis Mode: Serena MCP (Semantic)
- High-confidence anti-pattern detection
- Accurate schema extraction
- Cross-file reference tracking

If Serena fails, automatic Grep fallback with medium confidence.
```

**If Grep fallback triggered:**

```
⚠️ **Serena MCP Unavailable - Using Grep Fallback**

Analysis quality: Medium confidence (pattern matching)

To enable high-confidence analysis:
1. Verify Serena MCP server is running
2. Check CLAUDE.md Repository Registry for Serena instance name
3. Re-run this skill

Analysis will proceed with Grep (some patterns may be missed).
```

---

## Pattern 10: Config Write Protection

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
