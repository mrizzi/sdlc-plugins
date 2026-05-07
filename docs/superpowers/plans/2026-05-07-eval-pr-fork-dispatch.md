# Eval PR Fork Dispatch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split `eval-pr.yml` into a two-stage `workflow_run` dispatch pattern so fork PRs can run evals with secret access, gated by a collaborator trust check.

**Architecture:** Stage 1 (`eval-pr.yml`, `pull_request` trigger) discovers changed skills and uploads an artifact with PR metadata. Stage 2 (`eval-pr-run.yml`, `workflow_run` trigger) downloads the artifact, checks if the PR author is a trusted collaborator, gates untrusted authors behind a protected environment, then runs evals and posts the PR review.

**Tech Stack:** GitHub Actions, `actions/upload-artifact@v4`, `actions/download-artifact@v4`, `actions/github-script@v7`, GitHub REST API (collaborator permissions)

**Spec:** `docs/specs/2026-05-07-eval-pr-fork-dispatch-design.md`

---

### Task 1: Modify eval-pr.yml to discovery-only with artifact upload

Strip all secret-dependent steps (GCP auth, Claude Code install, eval execution, review posting) and add metadata write + artifact upload.

**Files:**
- Modify: `.github/workflows/eval-pr.yml`

- [ ] **Step 1: Rewrite eval-pr.yml**

Replace the entire file with the discovery-only version. The job is renamed from `eval-pr` to `discover` to reflect its new purpose. Permissions drop to `contents: read` only.

```yaml
# Discovers changed skills for PR evals and uploads metadata for the
# dispatch workflow (eval-pr-run.yml) to execute with secret access.
#
# See docs/specs/2026-05-07-eval-pr-fork-dispatch-design.md for full design.

name: Eval PR

on:
  pull_request:
    branches: [main]
    paths:
      - 'plugins/sdlc-workflow/skills/**/*.md'
      - 'evals/**/evals.json'
      - '.github/workflows/eval-pr.yml'

jobs:
  discover:
    name: Discover Changed Skills
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Discover changed skills
        id: discover
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
        run: |
          changed_files=$(git diff --name-only "$BASE_SHA"...HEAD)
          echo "Changed files:"
          echo "$changed_files"

          skills=""
          for file in $changed_files; do
            skill=""
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

          echo "skills=${skills}" >> "$GITHUB_OUTPUT"
          echo "Discovered changed skills with evals: ${skills:-none}"

      - name: Write PR metadata
        env:
          SKILLS: ${{ steps.discover.outputs.skills }}
        run: |
          jq -n \
            --arg skills "$SKILLS" \
            --argjson pr_number ${{ github.event.pull_request.number }} \
            --arg head_sha "${{ github.event.pull_request.head.sha }}" \
            --arg author "${{ github.event.pull_request.user.login }}" \
            '{skills: $skills, pr_number: $pr_number, head_sha: $head_sha, author: $author}' \
            > eval-pr-metadata.json
          cat eval-pr-metadata.json

      - name: Upload PR metadata
        uses: actions/upload-artifact@v4
        with:
          name: eval-pr-metadata
          path: eval-pr-metadata.json
```

- [ ] **Step 2: Validate YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/eval-pr.yml')); print('Valid YAML')"`

Expected: `Valid YAML`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/eval-pr.yml
git commit -m "refactor(ci): strip eval-pr.yml to discovery-only with artifact upload

Stage 1 of the workflow_run dispatch pattern for fork PR secret access.
Eval execution moves to eval-pr-run.yml (next commit)."
```

---

### Task 2: Create eval-pr-run.yml dispatch workflow

The new workflow with three jobs: `discover` (download artifact + trust check), `gate` (environment approval for untrusted authors), and `run-evals` (checkout PR, run evals, post review).

**Files:**
- Create: `.github/workflows/eval-pr-run.yml`

- [ ] **Step 1: Create eval-pr-run.yml**

```yaml
# Runs evals for PRs via workflow_run dispatch, enabling secret access
# for fork PRs. Pairs with eval-pr.yml (Stage 1: discovery).
#
# Trust model:
# - Collaborators with write/admin permission: evals run automatically
# - External contributors: require manual approval via eval-protected environment
#
# See docs/specs/2026-05-07-eval-pr-fork-dispatch-design.md for full design.

name: Eval PR Run

on:
  workflow_run:
    workflows: ["Eval PR"]
    types: [completed]

permissions:
  contents: read
  pull-requests: write
  actions: read

jobs:
  discover:
    name: Discover PR Context
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    outputs:
      skills: ${{ steps.metadata.outputs.skills }}
      pr_number: ${{ steps.metadata.outputs.pr_number }}
      head_sha: ${{ steps.metadata.outputs.head_sha }}
      author: ${{ steps.metadata.outputs.author }}
      trusted: ${{ steps.metadata.outputs.trusted }}
    steps:
      - name: Download PR metadata
        uses: actions/download-artifact@v4
        with:
          name: eval-pr-metadata
          run-id: ${{ github.event.workflow_run.id }}
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Parse metadata and check trust
        id: metadata
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const metadata = JSON.parse(fs.readFileSync('eval-pr-metadata.json', 'utf8'));

            core.setOutput('skills', metadata.skills);
            core.setOutput('pr_number', metadata.pr_number.toString());
            core.setOutput('head_sha', metadata.head_sha);
            core.setOutput('author', metadata.author);

            let trusted = false;
            try {
              const { data } = await github.rest.repos.getCollaboratorPermissionLevel({
                owner: context.repo.owner,
                repo: context.repo.repo,
                username: metadata.author
              });
              trusted = ['admin', 'write'].includes(data.permission);
              console.log(`Author ${metadata.author}: permission=${data.permission}, trusted=${trusted}`);
            } catch (e) {
              console.log(`Author ${metadata.author}: not a collaborator (${e.status}), trusted=false`);
            }

            core.setOutput('trusted', trusted.toString());

  gate:
    name: Approval Gate
    needs: discover
    if: needs.discover.outputs.trusted != 'true' && needs.discover.outputs.skills != ''
    runs-on: ubuntu-latest
    environment: eval-protected
    steps:
      - run: echo "Approved by reviewer"

  run-evals:
    name: Run PR Evals
    needs: [discover, gate]
    if: >-
      !cancelled() &&
      needs.discover.result == 'success' &&
      needs.discover.outputs.skills != '' &&
      (needs.discover.outputs.trusted == 'true' || needs.gate.result == 'success')
    runs-on: ubuntu-latest
    steps:
      - name: Checkout PR merge commit
        uses: actions/checkout@v4
        with:
          ref: refs/pull/${{ needs.discover.outputs.pr_number }}/merge
          fetch-depth: 0

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v3
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Install Claude Code
        run: curl -fsSL https://claude.ai/install.sh | bash

      - name: Run PR evals
        env:
          CLAUDE_CODE_USE_VERTEX: "1"
          CLOUD_ML_REGION: ${{ secrets.GCP_CLOUD_ML_REGION }}
          ANTHROPIC_DEFAULT_SONNET_MODEL: "claude-sonnet-4-6"
          ANTHROPIC_DEFAULT_OPUS_MODEL: "claude-opus-4-6"
          ANTHROPIC_MODEL: "claude-opus-4-6"
        run: |
          IFS=',' read -ra SKILLS <<< "${{ needs.discover.outputs.skills }}"

          for skill in "${SKILLS[@]}"; do
            eval_count=$(jq '.evals | length' "evals/${skill}/evals.json")
            workspace="/tmp/${skill}-eval-pr"
            mkdir -p "${workspace}"

            echo "=== Running PR evals for ${skill} (${eval_count} cases) ==="
            echo "Workspace: ${workspace}"

            claude -p "$(cat <<PROMPT
          Use the sdlc-workflow:run-evals skill for skill /${skill}.
          Evals path: evals/${skill}/evals.json
          Workspace: ${workspace}
          PROMPT
            )" --permission-mode dontAsk \
              --allowedTools Read Write Bash Skill Agent Glob \
              --verbose 2>&1 || {
              echo "::warning::PR eval run failed for ${skill} (exit $?)"
              continue
            }

            echo "--- Workspace contents ---"
            find "${workspace}" -type f 2>/dev/null | head -80 || true
          done

      - name: Post eval results review
        env:
          SKILLS_CSV: ${{ needs.discover.outputs.skills }}
          PR_NUMBER: ${{ needs.discover.outputs.pr_number }}
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const skills = process.env.SKILLS_CSV.split(',').filter(Boolean);
            const prNumber = parseInt(process.env.PR_NUMBER);

            let body = '';
            for (const skill of skills) {
              const summaryPath = `/tmp/${skill}-eval-pr/summary.md`;
              if (fs.existsSync(summaryPath)) {
                body += fs.readFileSync(summaryPath, 'utf8');
              } else {
                body += `### ${skill}\n\n> No results produced. See workflow logs.\n\n`;
              }
            }

            const pluginJson = JSON.parse(fs.readFileSync('plugins/sdlc-workflow/.claude-plugin/plugin.json', 'utf8'));
            const version = pluginJson.version;

            body += '---\n';
            body += `*Generated by [sdlc-workflow/run-evals](plugins/sdlc-workflow/skills/run-evals) v${version}*\n`;

            const { data: reviews } = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: prNumber
            });
            const marker = '## Eval Results';
            const existing = reviews.find(r =>
              r.user?.login === 'github-actions[bot]' && r.body?.startsWith(marker)
            );

            if (existing) {
              await github.rest.pulls.updateReview({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: prNumber,
                review_id: existing.id,
                body
              });
            } else {
              await github.rest.pulls.createReview({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: prNumber,
                event: 'COMMENT',
                body
              });
            }
```

- [ ] **Step 2: Validate YAML syntax**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/eval-pr-run.yml')); print('Valid YAML')"`

Expected: `Valid YAML`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/eval-pr-run.yml
git commit -m "feat(ci): add eval-pr-run.yml for fork PR eval dispatch

Stage 2 of the workflow_run dispatch pattern. Downloads PR metadata
from eval-pr.yml, gates untrusted authors via eval-protected environment,
then runs evals with secret access and posts the PR review."
```

---

### Task 3: Update existing spec with cross-reference

Add a reference from the original eval CI spec to the fork dispatch spec.

**Files:**
- Modify: `docs/specs/2026-04-21-eval-skills-ci-workflow-design.md`

- [ ] **Step 1: Add fork dispatch reference**

Add the following line at the end of the "Security Considerations" section (after line 168, before the "Out of Scope" heading):

```markdown
- Fork PR secret access is handled via `workflow_run` dispatch — see [Eval PR Fork Dispatch](2026-05-07-eval-pr-fork-dispatch-design.md).
```

- [ ] **Step 2: Commit**

```bash
git add docs/specs/2026-04-21-eval-skills-ci-workflow-design.md
git commit -m "docs(specs): add fork dispatch cross-reference to eval CI spec"
```

---

### Post-Implementation: GitHub Environment Setup

After merging, create the `eval-protected` environment in the repository:

1. Go to Settings > Environments > New environment
2. Name: `eval-protected`
3. Add required reviewers (repository maintainers)
4. No environment-specific secrets needed — existing repository-level secrets are used
