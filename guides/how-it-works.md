# How it works

The practices reach a project in four ways: **documents** people and agents
read, a **kit** of scripts synced into the project, **GitHub Actions** the
project calls, and a **Claude Code plugin** agents load. This page explains
each, who owns which file, and how a change here reaches every project.

## What flows where

```text
 dorhawk-software/practices                         a project (e.g. tern)
 ─────────────────────────                          ─────────────────────
 common/*.md, rust/*.md ── read, linked from ──────▶ CLAUDE.md (one line each)

 scripts/*, hooks/*  ──── bin/install ────────────▶ .practices/bin/*     synced
                          (or a sync PR)            .practices/hooks/*   synced
                                                    .practices/VERSION   synced
 templates/config ─────── first install only ─────▶ .practices/config    project's
 rust/templates/* ─────── --templates, if absent ─▶ clippy.toml, deny.toml,
                                                    rust-toolchain.toml,
                                                    .github/dependabot.yml,
                                                    .claude/settings.json  project's

 actions/*, .github/workflows/rust-*.yml ◀── uses: …@v1 ── .github/workflows/*.yml

 rust/templates/claude-settings.json ── --templates ─▶ .claude/settings.json
                                                    (PostToolUse ─▶ .practices/bin/claude-hook)

 .claude-plugin/marketplace.json ◀── /plugin install ── Claude Code
   plugin/ (skills only)

 projects.json ── sync-projects.yml ── opens a PR ──▶ each listed project
```

Every project gets the language-neutral part: `check-private`,
`check-commit-msg` and the git hooks that run them, with nothing to build
and no compiler called. A project with a `Cargo.toml` also gets the Rust
part: the coverage floors file, the templates, and the Rust checks the
pre-commit hook runs when Rust files are committed. Other languages have
no checks in the kit yet ([ROADMAP.md](../ROADMAP.md), phase 7).

The same scripts run in four places: by hand, in the git hooks, in the
Claude Code hook, and in CI. A check that passes on your machine passes in
CI for the same reason, and the other way round.

## The kit

`bin/install PROJECT_DIR` copies the kit into the project:

| Path in the project | Owner | Changed by |
| --- | --- | --- |
| `.practices/bin/` | the kit | every `bin/install` or sync PR replaces it whole |
| `.practices/hooks/` | the kit | the same |
| `.practices/VERSION` | the kit | the practices commit or tag it came from |
| `.practices/README.md` | the kit | says what's synced and what isn't |
| `.practices/config` | the project | created once from [templates/config](../templates/config), then never touched |
| `.practices/coverage-floors` | the project | created once with a header in a Rust project; you add the crates |
| `.practices/size-allowlist` | the project | you, when adopting the size limit ([adopt guide](adopt-in-a-rust-project.md)) |
| `.practices/lint.d/*` | the project | your own extra lint steps |

Commit `.practices/` whole. The project then works offline, on a fresh
clone, and in CI with no extra download, and a sync PR shows exactly what
changed in the scripts.

**Never edit `.practices/bin` in a project.** The next sync replaces it.
Change the script here, with a test in `tests/run`, and sync.

### The scripts

| Script | What it checks or does | Runs in |
| --- | --- | --- |
| `lint` | rustfmt, clippy, cargo deny, cargo machete, then the checks below and `lint.d/*` | Claude hook, pre-commit, CI |
| `check-private` | no name from `dev/private-terms` in files or the message; fails closed | lint, both git hooks |
| `check-size` | 700 lines per file, 1000 per integration test, the shrinking allowlist | lint |
| `check-unsafe` | `unsafe` only in `UNSAFE_ALLOWED` | lint |
| `check-coverage` | each crate at or over its floor, per OS; floors never lowered | pre-commit, CI |
| `check-commit-msg` | no session IDs or session links; no private names | commit-msg hook |
| `install-hooks` | points git at `.practices/hooks` (`--check` to verify) | once per clone; lint checks it |
| `claude-hook` | disk floor after every command; lint after cargo builds | Claude Code |
| `disk-guard` | keeps `DISK_FLOOR_GB` free where cargo builds | Claude hook |
| `prune-caches` | deletes GitHub caches a newer one of the same kind replaced | CI on main |
| `sweep-target` | keeps only the build units cargo used, before caching by hand | CI, packaging |

The settings each script reads are in [templates/config](../templates/config),
with their defaults in `scripts/lib.sh`.

### Project steps: `lint.d`

A check only one project needs goes in `.practices/lint.d/`, as an
executable file. `lint` runs each one after its own checks and shows its
output only when it fails. Crake's GPUI patch check and its magic-number
linter live there.

## Versions

- `.practices/VERSION` says which commit or tag of this repository the kit
  came from.
- Releases are tags: `v1.2.0` for each release, and a moving `v1` on the
  newest 1.x. A breaking change (a renamed input, a removed script) makes
  `v2`.
- Projects call the actions and workflows as `@v1`. They get fixes without
  a change of their own, and a breaking change only when they move to `@v2`.
- The kit in `.practices/` changes only through a sync PR, so a project
  never gets new script behaviour without seeing it in a diff.

## The sync

`projects.json` lists the repositories that take the kit:

```json
{ "projects": [
    { "repo": "dorhawk-software/crake" },
    { "repo": "dorhawk-software/tern" }
] }
```

`.github/workflows/sync-projects.yml` runs on each release (and by hand). For
each listed project it checks the repository out, runs `bin/install` on it,
and when anything changed, opens (or updates) a pull request. The project's
own CI then runs on that pull request, so a change here is proven in every
project before it lands there.

It needs the secret `PRACTICES_SYNC_TOKEN`: a fine-grained personal access
token limited to the listed repositories, with **Contents: read and write**
and **Pull requests: read and write**. Without it, the workflow says so and
does nothing.

## The reusable workflows

### `rust-ci.yml`

The whole Rust gate as one job: setup, lint, tests with coverage, and cache
pruning on the default branch.

```yaml
jobs:
  rust:
    permissions:
      contents: read
      actions: write
    uses: dorhawk-software/practices/.github/workflows/rust-ci.yml@v1
    with:
      gpui: true
    secrets:
      private-terms: ${{ secrets.PRIVATE_TERMS }}
```

| Input | Default | What it does |
| --- | --- | --- |
| `runs-on` | `'"ubuntu-24.04"'` | the runner, as a JSON string: `'["self-hosted", "linux"]'` for your own |
| `apt-packages` | empty | extra Debian packages the build needs |
| `gpui` | `false` | adds GPUI's X11, Wayland, fonts and Vulkan development packages |
| `coverage` | `true` | runs the tests through `check-coverage`; `false` runs plain `cargo test` |
| `coverage-extra` | empty | scripts run after the tests in the same instrumented build |
| `prune-caches` | `true` | deletes replaced caches after a run on the default branch |

| Secret | What it does |
| --- | --- |
| `private-terms` | the patterns `check-private` searches for in CI; without it the check says it skipped |

### `rust-advisories.yml`

`cargo deny check advisories`, on a schedule the project sets (daily is
right). A new advisory then shows up as one failed scheduled run, before it
turns every branch red at once.

### `rust-toolchain-bump.yml`

Weekly. When a newer stable Rust has been out for 14 days, it opens a pull
request that moves `rust-toolchain.toml` to it. It needs `contents: write`,
`pull-requests: write` and `actions: write` (a pull request opened with the
workflow's own token doesn't start CI by itself, so it starts CI on the
branch).

## The composite actions

The workflows are built from these. A project with a CI of its own (Crake,
with 18 jobs) uses them directly.

| Action | What it does |
| --- | --- |
| `actions/rust-setup` | apt packages with a time limit, the pinned toolchain, rust-cache saved by the default branch only, cargo tools |
| `actions/rust-lint` | `.practices/bin/lint`, with the private terms from a secret |
| `actions/rust-coverage` | `.practices/bin/check-coverage`, with the base ref for the never-lower check |
| `actions/prune-caches` | `.practices/bin/prune-caches` |

```yaml
steps:
  - uses: actions/checkout@v5
  - uses: dorhawk-software/practices/actions/rust-setup@v1
    with:
      gpui: true
      tools: cargo-deny,cargo-machete,cargo-llvm-cov
  - uses: dorhawk-software/practices/actions/rust-lint@v1
    with:
      private-terms: ${{ secrets.PRIVATE_TERMS }}
```

Why each step is there (main-only cache saves, the toolchain in the key,
time limits from measurements): [common/ci-caching.md](../common/ci-caching.md).

## The Claude Code hook

The lint and disk hook lives in each project's own `.claude/settings.json`,
copied from [rust/templates/claude-settings.json](../rust/templates/claude-settings.json)
by `bin/install --templates`:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.practices/bin/claude-hook",
        "timeout": 900
      }]
    }]
  }
}
```

After each shell command an agent runs, `claude-hook` checks the disk floor,
and after a cargo build, test, check, clippy, run or nextest it runs the lint
gate. A failure goes back to the agent as an error to fix before going on.
Because it is in the project, it works for anyone who opens the project in
Claude Code, with or without the plugin, and it never runs twice.

## The Claude Code plugin

This repository is also a Claude Code plugin marketplace,
`dorhawk-practices`, defined in `.claude-plugin/marketplace.json`. Its
plugin `practices` lives in `plugin/` and carries **skills only**:

- `adopt-practices`: walks an agent through the
  [adopt guide](adopt-in-a-rust-project.md) in a project.
- `fold-in-a-project`: runs the audit in
  [fold in a project](fold-in-a-project.md) on another codebase.
- `practices-gate`: what to do when the gate fails, and the rules that come
  with it (fix, never silence; the allowlist only shrinks).

Install it in Claude Code:

```text
/plugin marketplace add dorhawk-software/practices
/plugin install practices@dorhawk-practices
```
