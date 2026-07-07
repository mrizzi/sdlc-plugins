#!/usr/bin/env bash
# Reproducer test for TC-5101 / TC-5102: verifies that the eval-pr-run
# skill discovery script detects only PR-changed skills, not files
# introduced on main after the PR branch forked.
set -euo pipefail

WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

pass=0
fail=0

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "  PASS: $label"
    pass=$((pass + 1))
  else
    echo "  FAIL: $label"
    echo "    expected: $expected"
    echo "    actual:   $actual"
    fail=$((fail + 1))
  fi
}

# --- Setup: create a repo mimicking refs/pull/N/merge topology ---

cd "$WORK_DIR"
git init -q repo && cd repo
git config user.email "test@test.com"
git config user.name "Test"

# Initial commit on main with skill and eval structures
mkdir -p plugins/sdlc-workflow/skills/{alpha,beta,gamma}
mkdir -p evals/{alpha,beta,gamma}
for s in alpha beta gamma; do
  echo "skill $s" > "plugins/sdlc-workflow/skills/$s/SKILL.md"
  echo '{"evals":[]}' > "evals/$s/evals.json"
done
git add -A && git commit -q -m "init: add skills alpha, beta, gamma"

# Record the fork point (this is what pr.base.sha would return)
FORK_POINT=$(git rev-parse HEAD)

# Create the PR branch from this point
git checkout -q -b pr-branch

# PR changes only the "alpha" skill
echo "updated alpha" > plugins/sdlc-workflow/skills/alpha/SKILL.md
git add -A && git commit -q -m "pr: update alpha skill"
PR_HEAD=$(git rev-parse HEAD)

# Switch back to main and add a baseline commit touching ALL skills
git checkout -q main
for s in alpha beta gamma; do
  mkdir -p "evals/$s/baselines/abc123"
  echo "baseline" > "evals/$s/baselines/abc123/benchmark.json"
done
git add -A && git commit -q -m "chore(evals): create baselines for all skills"
MAIN_TIP=$(git rev-parse HEAD)

# Create a merge commit mimicking refs/pull/N/merge
git merge -q --no-ff pr-branch -m "Merge PR into main"

# --- Extract the discovery script from the workflow ---

discover() {
  local base_sha="$1"
  local changed_files
  changed_files=$(git diff --name-only "$base_sha"...HEAD)

  local skills=""
  for file in $changed_files; do
    local skill=""
    if [[ "$file" =~ ^plugins/sdlc-workflow/skills/([^/]+)/ ]]; then
      skill="${BASH_REMATCH[1]}"
    elif [[ "$file" =~ ^evals/([^/]+)/ ]]; then
      skill="${BASH_REMATCH[1]}"
    fi

    if [ -n "$skill" ] && [ -f "evals/${skill}/evals.json" ]; then
      if [[ ! ",$skills," == *",$skill,"* ]]; then
        skills="${skills:+${skills},}${skill}"
      fi
    fi
  done
  echo "$skills"
}

# --- Test 1: OLD approach (pr.base.sha = fork point) detects too many skills ---
echo "Test 1: Old approach (stale pr.base.sha) over-detects"
old_result=$(discover "$FORK_POINT")
# Sort for stable comparison
old_sorted=$(echo "$old_result" | tr ',' '\n' | sort | tr '\n' ',' | sed 's/,$//')
assert_eq "detects all three skills (bug)" "alpha,beta,gamma" "$old_sorted"

# --- Test 2: NEW approach (HEAD^1 = merge commit first parent) detects only PR skills ---
echo "Test 2: New approach (HEAD^1) detects only changed skill"
MERGE_PARENT=$(git rev-parse HEAD^1)
new_result=$(discover "$MERGE_PARENT")
assert_eq "detects only alpha" "alpha" "$new_result"

# --- Test 3: skill changes via evals/ path are also detected ---
echo "Test 3: Eval file changes detected via evals/ regex"
git checkout -q -b pr-branch-2 main
echo '{"evals":[{"name":"test"}]}' > evals/beta/evals.json
git add -A && git commit -q -m "pr: update beta evals"
git checkout -q main
git merge -q --no-ff pr-branch-2 -m "Merge PR 2 into main"
MERGE_PARENT_2=$(git rev-parse HEAD^1)
result_3=$(discover "$MERGE_PARENT_2")
assert_eq "detects only beta" "beta" "$result_3"

# --- Test 4: skill changes under plugins/ path are detected ---
echo "Test 4: Skill file changes detected via plugins/ regex"
git checkout -q -b pr-branch-3 main
echo "new content" > plugins/sdlc-workflow/skills/gamma/SKILL.md
git add -A && git commit -q -m "pr: update gamma skill"
git checkout -q main
git merge -q --no-ff pr-branch-3 -m "Merge PR 3 into main"
MERGE_PARENT_3=$(git rev-parse HEAD^1)
result_4=$(discover "$MERGE_PARENT_3")
assert_eq "detects only gamma" "gamma" "$result_4"

# --- Summary ---
echo ""
echo "Results: $pass passed, $fail failed"
if [ "$fail" -gt 0 ]; then
  exit 1
fi
