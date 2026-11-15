# Practices

The public source of truth for how dorhawk.software builds software:
practices (common/, ui/ and one folder per language), and the kit that
enforces them (scripts/, hooks/, actions/, .github/workflows/, plugin/).
README.md is the map; read it first.

## Rules for this repository

- **Documentation is the product** (the owner, 2026-11-11: "extremely well
  documented with examples, guides, todos"). A change to the kit changes
  its doc, guide, example and ROADMAP.md in the same commit, and adds a
  line under "Unreleased" in CHANGELOG.md.
- **Every practice has four parts**: What, Why (the incident, its cost,
  and a link to the commit that paid for it), Apply, Check. No essays:
  plain words, sentences under 25 words.
- **Every rule a machine can check is a gate the agent can't skip** (the
  owner, 2026-11-15, after a board was called ready with a button
  sticking out of its panel: the rule was written, nothing measured it).
  A rule's Check names the script that enforces it and where it runs:
  claude-hook after edits and before the agent's turn ends, the git
  hooks, CI. Its findings go back to the agent, each with its fix
  ([common/gates.md](common/gates.md)). Only judgement (taste, wording,
  whether an icon is ugly) is left to reviewers, and the Check says so.
  - A new or changed rule gets its row in [ENFORCEMENT.md](ENFORCEMENT.md):
    gate, partial, todo or review. `tests/enforcement` fails without it.
  - A rule a script could check, but none does yet, is a todo there and
    a task in ROADMAP.md, in the same commit.
  - A new check comes with a planted fault in tests/run (it must catch
    it, on its own rule) and a mutant in tests/mutate (breaking the
    check must fail that case).
- **Public repository.** No client or company names from private work,
  no real hosts or non-documentation addresses, no email addresses or
  account names, no people's names (roles only). Examples use ACME,
  Globex, Initech, `*.example`, 192.0.2.x / 198.51.100.x / 203.0.113.x.
- **The checkers are tested.** A change to a script in scripts/ or hooks/
  comes with a case in tests/run that fails without it. Scripts run on
  bash 3.2 (macOS) and BSD tools: no mapfile, no associative arrays, no
  GNU-only flags. A check that can't do its work fails; it never says
  "clean".
- **Pin third-party actions by commit SHA** (with the version in a
  comment), choosing releases at least two weeks old.
- **Never break `@v1`.** A change that would break a project using the
  actions or workflows is a new major version.
- **A release moves the plugin's version too**: plugin.json and
  marketplace.json say the release's version, in the release commit.
- Commits: the subject is the outcome; the body says why. Co-Authored-By
  is fine; never a session ID or session link (CI refuses them).

## Checks

```sh
tests/check     # the gate: shellcheck, links, readme, versions, enforcement, tests/run
tests/run       # the kit's checks on throwaway projects (seconds)
tests/mutate    # each check broken in a copy: tests/run must fail on its case (minutes)
tests/enforcement # ENFORCEMENT.md classifies every rule of every practice
tests/links     # every relative link in the docs resolves
tests/readme    # README names every top-level entry, practice, guide and script
tests/versions  # the plugin's version is the newest release in CHANGELOG.md
tests/example   # the kit end to end on examples/rust-workspace (needs Rust)
```

The pre-commit hook runs `tests/check` (once per clone:
`git config core.hooksPath .githooks`). Until 2026-11-12 the checks ran
only in CI, and a commit that failed shellcheck reached main.

CI (.github/workflows/ci.yml) runs all of them, tests/run on Linux and
macOS, tests/mutate on macOS, plus actionlint and the commit-message
check. tests/run and tests/mutate need Node and Chrome (check-ui renders
boards); without them they fail, as the gate does.

## Adding a practice or a project

guides/fold-in-a-project.md. Next in line: Obálka (React Native, a
`typescript/` folder) and the dorhawk.software website (`web/`).
