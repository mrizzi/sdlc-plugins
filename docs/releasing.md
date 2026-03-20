# Releasing

This document describes how to release a new version of the sdlc-workflow plugin.

## Release Process

1. **Develop on a branch** — make skill/plugin changes on a feature branch, open a PR, get it reviewed, and merge to the default branch.

2. **Bump the version** — update the `version` field in **both** of these files (they must stay in sync):
   - `.claude-plugin/marketplace.json` — required by Claude Code for relative-path plugins to detect available updates (see [version resolution](https://code.claude.com/docs/en/plugin-marketplaces#version-resolution-and-release-channels))
   - `plugins/sdlc-workflow/.claude-plugin/plugin.json` — required to pass `claude plugin validate` without warnings

   Follow [Semantic Versioning](https://semver.org/) using the decision criteria in the [Version Bump Decision Guide](#version-bump-decision-guide) below:
   - `0.X.0` → `0.(X+1).0` (y-stream) for new features or breaking changes
   - `0.X.Y` → `0.X.(Y+1)` (z-stream) for enhancements, bug fixes, and polish

3. **Commit the version bump** with the message:
   ```
   chore(release): bump version to X.Y.Z
   ```

4. **Push to the default branch.**

5. **Create a GitHub release** — tag the release commit and create a GitHub release with notes from the changelog:
   ```bash
   git tag vX.Y.Z <commit-sha>
   git push origin vX.Y.Z
   gh release create vX.Y.Z --title "vX.Y.Z" --latest --notes "<changelog section for this version>"
   ```
   Use the corresponding `CHANGELOG.md` section as the release notes body.

6. **Users update** by running:
   ```
   /plugin marketplace update
   ```

## Version Bump Decision Guide

The version bump decision is a **human judgment call**, not a mechanical scan of commit prefixes. A commit tagged `feat` does not automatically mean a y-stream bump — many `feat` commits are enhancements to existing functionality and belong in a z-stream release.

### Decision checklist

Ask these questions about the changes since the last release:

| Question | If yes |
|---|---|
| Does this release introduce a **new skill** (e.g. `verify-pr`, `plan-feature`)? | y-stream |
| Does it add a **new workflow phase** or fundamentally change the SDLC methodology? | y-stream |
| Does it introduce a **breaking change** to the task template contract, plugin manifest, or project configuration? | y-stream |
| Does it improve an **existing skill's output**, formatting, or prompts? | z-stream |
| Does it add guidance, guardrails, or documentation to an existing skill? | z-stream |
| Is it a bug fix, typo correction, or documentation update? | z-stream |

If none of the y-stream criteria apply, use a z-stream bump — even if every commit uses the `feat` prefix.

### Examples

These examples use real commit messages from this project to illustrate the distinction:

**z-stream (`feat` commits that are enhancements, not new features):**

- `feat(skills): enhance comment footer with plugin link, skill name, and version` — improves existing comment output formatting; no new capability is introduced
- `feat(skills): add CONVENTIONS.md fill-in prompt to setup skill` — adds a prompt to an existing skill; the skill itself already exists
- `feat(skills): add loop detection guidance to implement-task` — adds guardrails to an existing skill's instructions

**y-stream (genuinely new features or breaking changes):**

- `feat(skills): add verify-pr skill for PR verification against Jira tasks` — introduces an entirely new skill that didn't exist before
- `feat(plan-feature): add constraint-aware task generation` — adds a new capability (constraint awareness) that changes how tasks are generated, altering the task template output

## Versioning Rules

- The version in `marketplace.json` is what Claude Code uses to detect whether an update is available for relative-path plugins. If the version doesn't change, `/plugin marketplace update` will skip the plugin even if files have changed.
- The version in `plugin.json` is required by `claude plugin validate` — omitting it produces a warning. It must match `marketplace.json` to stay consistent.
- This project uses relative-path plugin sources (`"source": "./plugins/sdlc-workflow"`). In the future, it can migrate to GitHub-sourced plugins for tag-based pinning and independent versioning per plugin.
