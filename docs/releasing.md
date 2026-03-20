# Releasing

This document describes how to release a new version of the sdlc-workflow plugin.

## Release Process

1. **Develop on a branch** — make skill/plugin changes on a feature branch, open a PR, get it reviewed, and merge to the default branch.

2. **Bump the version** — update the `version` field in **both** of these files (they must stay in sync):
   - `.claude-plugin/marketplace.json` — required by Claude Code for relative-path plugins to detect available updates (see [version resolution](https://code.claude.com/docs/en/plugin-marketplaces#version-resolution-and-release-channels))
   - `plugins/sdlc-workflow/.claude-plugin/plugin.json` — required to pass `claude plugin validate` without warnings

   Follow [Semantic Versioning](https://semver.org/):
   - `0.X.0` → `0.(X+1).0` for new features or breaking changes
   - `0.X.Y` → `0.X.(Y+1)` for bug fixes

3. **Commit the version bump** with the message:
   ```
   chore(release): bump version to X.Y.Z
   ```

4. **Push to the default branch.**

5. **Users update** by running:
   ```
   /plugin marketplace update
   ```

## Versioning Rules

- The version in `marketplace.json` is what Claude Code uses to detect whether an update is available for relative-path plugins. If the version doesn't change, `/plugin marketplace update` will skip the plugin even if files have changed.
- The version in `plugin.json` is required by `claude plugin validate` — omitting it produces a warning. It must match `marketplace.json` to stay consistent.
- This project uses relative-path plugin sources (`"source": "./plugins/sdlc-workflow"`). In the future, it can migrate to GitHub-sourced plugins for tag-based pinning and independent versioning per plugin.
