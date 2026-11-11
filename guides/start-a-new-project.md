# Start a new project

Everything a new repository gets on its first day, in order, so the rules
hold from the first commit instead of being adopted later. Adopting later
costs far more: see [adopt in a Rust project](adopt-in-a-rust-project.md)
for what that takes.

The [example workspace](../examples/rust-workspace/) is the result of this
guide for a Rust project. Copy from it freely.

## 1. The repository and who commits

```sh
mkdir acme-app && cd acme-app
git init -b main
git config user.email you@your-domain.example   # this repository's identity, set here
git config user.name "Your Name"
```

- One commit identity per repository, set in the repository's own config,
  not taken from whatever the machine's global one is
  ([common/commits.md](../common/commits.md)).
- Decide now whether the repository is public. A public one needs the
  privacy setup in step 3 before anything else is written. A private one
  pays for CI minutes (step 6).
- Write down who may push, and when ("once work is done and tested"), in
  CLAUDE.md. An agent never assumes it.

## 2. CLAUDE.md: rules and pointers

CLAUDE.md is read whole by every agent request, so it holds the rules and a
one-line pointer per area. The detail goes to `docs/engineering/`
([common/claude-md.md](../common/claude-md.md)).

```markdown
# Acme App

One paragraph: what it is, who it's for, what it never does.

## Git rules
- Commit as the repository's configured identity.
- No session IDs or session links in commits (the commit-msg hook refuses them).
- Push once work is done and tested.

## Read first
- docs/engineering/: the detail behind each section here.

## Practices (github.com/dorhawk-software/practices)
- Lints are errors: `.practices/bin/lint`; never silence one.
- Tests never touch this computer: common/testing.md.
- Whatever is decided "not now" goes in docs/engineering/not-now.md, same commit.
- Every user-facing change adds a CHANGELOG line under Unreleased, same commit.
```

Every rule records where it came from and when: "(asked for 2026-11-11)".
An agent can then tell a hard rule from a past choice.

## 3. Privacy, before the first real name

Even a private repository may go public one day, and examples get copied.

```sh
printf 'CLAUDE.local.md\ndev/private-terms\ntarget/\n' >.gitignore
mkdir -p dev
printf '# names never to commit (clients, hosts, addresses), one PCRE pattern per line\n' >dev/private-terms
```

- Code, tests, demo data and docs use made-up names (ACME, Globex, Initech),
  `*.example` and `*.internal` hosts, and documentation addresses
  (192.0.2.x, 198.51.100.x, 203.0.113.x).
- What you learn on real systems goes in `CLAUDE.local.md`, which git
  ignores.
- The hooks refuse any commit, or commit message, that matches
  `dev/private-terms`
  ([common/privacy-public-repos.md](../common/privacy-public-repos.md)).
- Nothing private at all? Set `PRIVATE_TERMS=none` in `.practices/config`
  instead. The check never decides that on its own.

## 4. The workspace

```toml
# Cargo.toml
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.package]
version = "0.1.0"
edition = "2024"
license = "MIT"
publish = false
```

Each crate inherits `version`, `edition`, `license` and `publish`, and opts
into the workspace lints. Shared dependencies go in
`[workspace.dependencies]` from the start
([rust/conventions.md](../rust/conventions.md)).

## 5. The kit, with its templates

```sh
~/src/practices/bin/install --templates .
```

Then paste the printed `[workspace.lints]` block into `Cargo.toml`, and:

```sh
$EDITOR deny.toml                 # keep the licence list for your licence
$EDITOR rust-toolchain.toml       # today's stable: rustc --version
.practices/bin/install-hooks
for c in crates/*; do printf '%-24s 0 0\n' "$c"; done >>.practices/coverage-floors
nice -n 19 cargo build && .practices/bin/lint
```

On a new project, every check passes on the first run. Keep it that way:
raise the coverage floors as soon as the first tests exist
([rust/coverage.md](../rust/coverage.md)).

## 6. CI

Copy the three workflows from the example:
[ci.yml](../examples/rust-workspace/.github/workflows/ci.yml),
[advisories.yml](../examples/rust-workspace/.github/workflows/advisories.yml),
[toolchain.yml](../examples/rust-workspace/.github/workflows/toolchain.yml),
and the template [dependabot.yml](../rust/templates/dependabot.yml) (already
copied by `--templates`).

- **Public repository:** standard runners are free. Add the other systems
  you ship for as jobs of their own.
- **Private repository:** one Linux job, `paths-ignore` for docs, and the
  local hooks as the real gate
  ([common/ci-caching.md](../common/ci-caching.md)).
- Secrets: `PRIVATE_TERMS` (the same patterns as `dev/private-terms`) so CI
  checks names too. Without it, CI says it skipped the check.

## 7. CHANGELOG.md, with its kinds

```markdown
# Changelog

## Unreleased

### New
### Better
### Changed
### Fixed
### Underneath
```

Written by hand, for the people using the app, in its own voice. Every
user-facing change adds a line in the same commit, dependency updates too
([common/changelog.md](../common/changelog.md)). Releases follow
[common/releases.md](../common/releases.md).

## 8. not-now.md

```sh
mkdir -p docs/engineering
printf '# Not now\n\nWhat we decided not to do yet, and why. Done items leave the list.\n' >docs/engineering/not-now.md
```

From the first day: whatever is decided "not now" is written down here, or
next to the code, in the same commit ([common/not-now.md](../common/not-now.md)).

## 9. The first commit

```sh
git add -A
git commit -m "Acme App: <what it is, in one sentence>" -m "<why it exists, what it does first>"
```

The pre-commit hook runs the lint gate and coverage. The commit-msg hook
reads the message ([common/commits.md](../common/commits.md)).

## Checklist

- [ ] `git config user.email` set in this repository
- [ ] Public or private decided; push permission written in CLAUDE.md
- [ ] CLAUDE.md with rules and pointers; `docs/engineering/` exists
- [ ] `.gitignore` has `CLAUDE.local.md`, `dev/private-terms`, `target/`
- [ ] `dev/private-terms` exists (or `PRIVATE_TERMS=none` in `.practices/config`)
- [ ] Workspace: resolver 3, edition 2024, `[workspace.package]`, `publish = false`
- [ ] `bin/install --templates` run; lints pasted; each crate has `[lints] workspace = true`
- [ ] `deny.toml` keeps one licence list; `rust-toolchain.toml` pinned
- [ ] `.practices/bin/install-hooks` run; `.practices/bin/lint` passes
- [ ] Coverage floors set, raised once tests exist
- [ ] `ci.yml`, `advisories.yml`, `toolchain.yml`, `dependabot.yml`
- [ ] `PRIVATE_TERMS` secret set in the repository
- [ ] `CHANGELOG.md` with Unreleased and the five kinds
- [ ] `docs/engineering/not-now.md`
- [ ] The first commit goes through both hooks
