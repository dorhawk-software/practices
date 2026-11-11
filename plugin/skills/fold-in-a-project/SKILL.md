---
name: fold-in-a-project
description: Audit a project's whole history and code for development practices worth sharing, then move them into the dorhawk-software/practices repository (common or per-language), the way Crake's were. Use when the person wants to fold a project's conventions (e.g. a React Native app, a website) into the practices, or asks for an audit of what a project learned.
---

# Fold a project's practices in

The full procedure: https://github.com/dorhawk-software/practices/blob/main/guides/fold-in-a-project.md.
In short:

## 1. Audit, in parallel

Six areas, one agent each, reading the files AND the git history (why
each piece exists, what broke, what was tried and reverted, the person's
dated rules):
1. CI and automation (workflows, caching, runners, secrets, bots)
2. Lints and static verification (configs, scripts, hooks)
3. Testing (suites, harnesses, fixtures, what never touches the machine)
4. Releases, versioning, packaging, distribution
5. Process from the whole commit history (message style, rules with
   dates, bug class -> guard, reverts, documentation layout)
6. Code conventions (layout, errors, logging, config, platform code)

Plus a seventh source no agent sees: the agent memory for that project
(the person's working rules), read yourself.

Every brief carries the privacy rule: the project's local notes and
private-terms list are not read, and any real client name, host,
non-documentation address or person's name is written "[private]". The
practices repository is public.

Each report gives, per practice: path, why (with commit), generality
(any project / language / framework / project-only), extraction form
(doc, script, action, workflow, template, tool), what to parameterise,
maturity and known problems; then a ranked copy-first list.

## 2. Decide with the person

One document: what the project has, the repo's shape for it, what copies
first, what to fix on the way, what stays, the decisions. Nothing moves
before the person agrees.

## 3. Move it

- Copy the chosen files verbatim in one commit (with a FROM-<PROJECT>.md
  saying from which commit), then generalise in the next commits, with
  tests that fail before each fix. The diffs then show what changed.
- A new language gets its own folder mirroring rust/ (conventions.md,
  lints.md, coverage.md, templates/), and its own actions and workflows.
- Every practice: what, why (with a link to the source commit), apply,
  check, and an example.
- Prove it by switching the source project to the shared version first;
  only then adopt it elsewhere.
- Update README.md's index, ROADMAP.md and CHANGELOG.md in the same commit.
