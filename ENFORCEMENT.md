# Enforcement

Every rule a machine can check is enforced by a gate the agent can't
skip: a script run by claude-hook (after each edit, and before an
agent's turn ends), by the git hooks, or in CI, whose findings go back
to the agent to fix. This is where each rule stands
([CLAUDE.md](CLAUDE.md), "Every rule a machine can check is a gate").

- **gate**: enforced; the script and where it runs.
- **partial**: part is enforced; the rest is the next check to build.
- **todo**: a machine could check it, and nothing does yet.
- **review**: it needs a person's judgement (taste, wording, whether
  an icon is ugly); reviewers check it.

Today: 15 gate, 79 partial, 130 todo, 49 review
(audited rule by rule on 2026-11-15, each claim checked against the
scripts, not the docs). `tests/enforcement` fails when a practice has a
rule this file doesn't list, or lists one that's gone. The todo and
partial rows are the work list; [ROADMAP.md](ROADMAP.md) ranks it.

## Any project (common/)

### [common/agent-working-rules.md](common/agent-working-rules.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Builds run at the lowest priority | partial | claude-hook and pre-commit run their own lint/coverage under nice -n 19 | The agent's own heavy commands (cargo/npm/xcodebuild/gradlew/docker, git commit) are not checked: a PreToolUse Bash hook should refuse them unless prefixed with nice -n 19. |
| The disk keeps a floor | partial | claude-hook runs disk-guard after every Bash command (exit 2 to the agent) | disk-guard exits 0 in any project without Cargo.toml (mobile/JS builds, Xcode DerivedData, Gradle unguarded), and lint never checks that .claude/settings.json actually registers claude-hook (install adds it only with --templates; the plugin ships no hooks). |
| Never a new target directory | todo | - | A PreToolUse Bash hook (claude-hook) should refuse commands that set CARGO_TARGET_DIR or pass --target-dir outside the project's target/, and disk-guard could list new top-level folders on the build disk. |
| Never `nix … path:` on a repo with a target folder | todo | - | A lint.d grep for flake references written as path: in scripts/ and .github/, plus a PreToolUse refusal of `nix ... path:` commands; nothing in the kit does either. |
| Builds go to the build disk | todo | - | A PreToolUse hook should refuse CARGO_BUILD_BUILD_DIR/CARGO_TARGET_DIR/--target-dir overrides, and disk-guard should fail when a configured BUILD_DISK is set but cargo metadata's build_directory is not under it. |
| Development builds aren't installed | review | - | Whether an instruction to the developer installs something is in the agent's chat messages, not in files a script sees. |
| Rebuild before saying "restart" | todo | - | A Stop hook could compare target/debug/<app> mtime with the newest changed source and fail with "rebuild first" when the binary is older. |
| Release only on a green main | todo | - | The kit ships no release script; a shared release script and release workflow job should refuse unless `gh run list --commit $SHA --status success` covers every job on main's tip. |
| Quote measured CI timings | review | - | A duration quoted in a chat message and its source are only visible to a reader of the conversation. |
| Keep going on an agreed plan | review | - | Whether a stop was for a question only the developer could answer is judgement. |
| Screenshots don't flash the screen | todo | - | A PreToolUse Bash hook could count desktop-portal/full-screen capture commands (gnome-screenshot, screencapture without -l/-R, portal calls) and refuse past two per session; low value. |
| Long gates run in the main session | review | - | Which agents run, and whether a sub-agent waited on a long gate, is visible only to the session that started them. |
| Only the lock's own script waits for the lock | todo | - | A PreToolUse claude-hook could refuse a Bash command that polls a `*.lock` path in a loop (`until [ ! -d …lock ]`, `while [ -e …lock ]`). |
| Write down what is deferred | review | - | Deciding what was deferred is judgement; the mechanical parts are the not-now.md rules. |
| Simulators run one at a time until the machine is measured | todo | - | A PreToolUse claude-hook could refuse `xcrun simctl boot` (or a second emulator) while another device is booted (`xcrun simctl list devices booted`), unless the project's config names a measured limit. |
| Don't edit a script while it runs | todo | - | A PreToolUse claude-hook could refuse an Edit or Write to a shell script that a running process executes (`pgrep -f <path>`). |

### [common/changelog.md](common/changelog.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Written for users, in the product's voice | review | - | Product voice and whether a user would understand the line need a reader (the bold-headline format is covered by the Fixed kinds parser todo). |
| Fixed kinds | todo | - | No kit script parses CHANGELOG.md: a lint step should refuse any ### heading outside New/Better/Changed/Fixed/Underneath (in that order) and any bullet not shaped `- **headline** body`, run by lint (claude-hook, pre-commit, CI). |
| Same commit, dependency updates too | todo | - | The doc itself says neither check exists: CI/pre-commit should fail a diff touching Cargo.lock/package-lock.json/Podfile.lock/gradle lockfiles that doesn't touch CHANGELOG's Unreleased section, and fail when a released section differs from its text at that release's tag. |
| The changelog is the release notes and What's new | todo | - | No kit release workflow: it should build the GitHub release body from the version's section and fail if they differ; the include_str! parse test is the project's own. |

### [common/ci-caching.md](common/ci-caching.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| The workflow header | partial | kit's own reusable workflows declare permissions contents: read; rust-setup sets CARGO_TERM_COLOR and line-tables-only | Nothing checks a project's own workflow headers: a workflow lint (lint.d or CI) should require branches-ignore dependabot/**, concurrency with cancel-in-progress: true and top-level permissions: contents: read. |
| Private repos: CI minutes are a budget | partial | pre-commit and claude-hook run the same lint/coverage locally; lint checks git hooks are installed | Nothing checks, for a private repo (gh api visibility), that macOS/Windows jobs run only on tags or workflow_dispatch and docs-only pushes are skipped; the monthly billing read stays human. |
| Caches are saved by main only | partial | actions/rust-setup saves its cache only on the default branch (save-cache: main) | Hand-written actions/cache or actions/cache/save steps are not checked: a workflow lint should require an if: on the default branch for every cache save. |
| Spend the 10 GB on purpose | partial | actions/rust-setup sets CARGO_PROFILE_DEV_DEBUG=line-tables-only | Total cache size is not measured: the prune-caches job could sum `gh cache list` sizes and fail above a headroom threshold (e.g. 8 GB). |
| The toolchain version is in the cache key | partial | actions/rust-setup uses Swatinem/rust-cache, whose key includes the rustc version | Hand-written cache keys are unchecked: a workflow lint should require a toolchain-version expression in every actions/cache key. |
| Prune the caches a newer one replaced | partial | rust-ci.yml's caches job runs actions/prune-caches after check on the default branch | In a project's own workflows nothing verifies the prune job's needs: lists every job that saves a cache. |
| Sweep target directories you cache by hand | todo | - | sweep-target ships but nothing requires it: a workflow lint should require a sweep-target step before any actions/cache save of a target/ path. |
| One build per job | partial | rust-ci.yml builds and tests in one job; check-coverage runs extra scripts in the same build | No check on a project's workflows or logs: refuse `cargo test -p`/`cargo build -p` in workflows, or count "Compiling <workspace crate>" once per job log. |
| Split the slowest suite, not the whole run | todo | - | A scheduled report job could read `gh run view --json jobs` and warn when the longest job exceeds 1.3x the second longest; low value. |
| Time limits come from measurements | partial | rust-ci check job has timeout-minutes; rust-setup wraps apt in timeout 300/900 | A project's own jobs and network steps are not checked for timeout-minutes; the measured-at comment stays a review item. |
| Artifacts are named per attempt | todo | - | A workflow lint should require ${{ github.run_attempt }} in every upload-artifact name that a download-artifact in another job reads. |
| Secrets reach only the steps that need them | todo | - | A workflow lint should refuse secrets. in workflow/job-level env and in step env of steps that run cargo/npm/gradle; note actions/rust-lint itself puts the private-terms secret in the env of the step that runs cargo clippy (build scripts can read it). |
| Pin third-party actions by commit | todo | - | No test enforces it in this repo (actionlint doesn't): tests/check should fail on any uses: whose ref isn't a 40-hex SHA except ./ and dorhawk-software/practices; the doc's own grep would match the practices@v1 lines. |

### [common/claude-md.md](common/claude-md.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Rules and pointers in CLAUDE.md; detail in docs/engineering | todo | - | Size part is checkable: lint should fail when CLAUDE.md exceeds a configured CLAUDE_MD_MAX characters (rule vs detail stays with review). |
| A handoff file is not a CLAUDE.md | review | - | Telling a standing rule from history or a deferral in a handoff file needs reading. |
| Every rule records its origin | todo | - | A pre-commit/lint.d check on CLAUDE.md's diff could require every added line with never/always/must to carry a date (YYYY-MM-DD) or "decided/asked for/chosen"; heuristic but deterministic. |
| The owner's words, quoted and dated | todo | - | A lint.d check that every feature record (configured spec glob) starts with `**Input**: Owner, YYYY-MM-DD: "...".` |
| Known gaps beside the rule, not a reworded rule | review | - | Whether the product falls short of a principle, and the wording stays as decided, needs judgement; only the dated "> Known gap (date)" shape is mechanical. |
| "Until <date>" notes keep the old behaviour visible | review | - | Whether a change altered behaviour and the old one is recorded needs reading the change. |
| Milestones say what was built and how it was proven | todo | - | Structure is checkable: each milestone part in docs/engineering/milestones.md has Built/Proven by/Found/Deferred lines and names a test path that exists; content quality stays review. |
| Tried by real people: a checklist per platform | review | - | Whether real people tried the software is a human fact; only the file's existence and tick format are mechanical. |

### [common/commits.md](common/commits.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| The subject is the outcome | todo | - | check-commit-msg checks only session IDs and private terms: it should refuse a subject over ~72 characters or a conventional prefix (feat:/fix:/chore:...), allowing CI:/Release:/Tests:/Scripts:; outcome wording stays review. |
| The body says why, with numbers, and how it was proven | review | - | Whether the body explains why and how it was proven needs a reader. |
| Co-Authored-By yes, session IDs never | partial | commit-msg hook (check-commit-msg); lint fails when hooks aren't installed (not in CI); this repo's ci.yml re-checks pushed commits | rust-ci.yml never re-checks pushed commit messages, so --no-verify commits pass in projects; PR descriptions are never checked; a present Co-Authored-By trailer on agent commits is not required. |
| Stable IDs survive a rewritten history | review | - | Whether a commit implements a feature record, and which ID it should cite, is judgement. |
| Trailers come last | todo | - | check-commit-msg should require that any Co-Authored-By line is printed by `git interpret-trailers --parse` (nothing after the trailer block), run in commit-msg and CI. |
| One commit identity per repository | todo | - | pre-commit/lint should fail when `git config --local user.email` is unset or differs from a GIT_EMAIL in .practices/config, and CI should check the pushed commits' author emails. |
| Pushing is stated, not assumed | todo | - | lint could check that CLAUDE.md has a Git rules section with a line about pushing; whether it fully answers "may I push?" stays review. |
| Release commits are just the version | todo | - | No kit release script/workflow: on a v* tag, CI should check the subject is `<Product> X.Y.Z` and `git show --stat` touches only configured version files and CHANGELOG.md. |

### [common/crash-reports.md](common/crash-reports.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Consent first: nothing starts before the user agrees | todo | - | A project-written check (fresh-install network capture, or a guard that the crash SDK's init is only called from the consent module); nothing in the kit. |
| Check every hook in the vendor's code, not its docs | review | - | Finding every data path an SDK has means reading the vendor's source; the per-kind test is project-written. |
| An allow-list scrubber, seeded with what the device knows | todo | - | A project test feeding each seeded identifier through the scrubber; nothing in the kit. |
| Three tiers, three rules | todo | - | Partly mechanical: eslint no-console as an error and a guard that the debug-tier folder imports no network API; nothing in the kit checks either. |
| Expected refusals aren't reported | todo | - | A project test per refusal code plus one other code still reported; nothing in the kit. |

### [common/gates.md](common/gates.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Prove the gate can fail | partial | tests/run and tests/example (this repo's pre-commit and CI) prove each kit checker fails on its fault | In projects nothing runs a canary: lint should run check-private against a planted term and each lint.d check against planted bad input, failing if any passes. |
| Every finding says how to fix it | partial | Kit scripts print the fix in their messages; tests/run checks exit codes | No test asserts any message's text (fix/why parts), and nothing checks project lint rules' messages. |
| A rule a machine can check runs where the agent can't skip it | partial | check-hooks (pre-commit) fails when .claude/settings.json stops running claude-hook after edits or on Stop; tests/enforcement fails when a rule here goes unclassified | The todo rows in this file: each is a check still to build. |
| A new check is broken once, then trusted | partial | check-proven, run by check-commit-msg (the commit-msg hook): a commit that adds or changes a file in CHECK_FILES carries a Proven: line of three words or more; this repository's own commit-msg hook sets CHECK_FILES to the kit's scripts and hooks | Whether the break was really tried and failed on the check's own case is review. CI's pushed-commit check doesn't know a commit's files, so a commit made with --no-verify isn't asked. A lint for a stored mutation suite (a mutants list, a SHARD) was left out: once the kit's list was gone it would match only unrelated words. |
| A rule is an error, or it's off with a reason | partial | rust/templates/Cargo-lints.toml makes all clippy lints and warnings deny | lint never verifies Cargo.toml has [workspace.lints] with warnings=deny and every crate `[lints] workspace = true` (install only prints it), so clippy warnings pass; no check for warn levels in eslint configs or reasons on #[allow]/eslint-disable. |
| The gate visits every file | partial | check-size and check-private walk git ls-files; clippy --all-targets and cargo fmt --all | No check that tsc/eslint's file list matches git ls-files for JS/TS; .rs files outside any module tree aren't seen by fmt/clippy; shell scripts in projects aren't linted at all. |
| A subset iterates; only the full run gates | review | - | Whether a claim or a merge rested on a partial run is in the conversation; the project's own hooks run the full set. |
| Cache by content, never by time | review | - | What a cached result is made of is each gate's own; the proofs (a design-only change caught without the simulator, a code change reshot, kept files byte-identical) are read in the commit. |
| A slow gate prints each phase's time | todo | - | check-ui and check-ui-tests could print each phase's time and the total, and tests/run assert the lines. |
| A ratchet for a rule you can't meet yet | partial | check-size's .practices/size-allowlist ratchet (lint: claude-hook, pre-commit, CI) | No generic baseline-of-counts helper for other countable rules (lint findings, skips, todo! counts). |
| A size limit is met by splitting, never by trimming | review | - | Whether user text was shortened or a plural dropped to fit needs reading the diff. |
| Audit only what ships; re-check every accepted advisory | partial | cargo deny advisories in lint (claude-hook, pre-commit, CI) and daily rust-advisories.yml | deny.toml ignore entries need no reason or expiry check, dev-dependencies aren't excluded, and there is no shipped-bundle audit for npm. |
| Licence notices from what ships; anything unknown fails | partial | cargo deny licences allow-list (unknown licence fails) in lint/CI | No generated notices file committed and regenerated-diffed in CI, and hand-listed native/font/vendored components aren't checked. |

### [common/it-just-works.md](common/it-just-works.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| The product decides, not the user | review | - | Which choices a signal could make for the user is product design. |
| Settings are preferences, not workarounds | review | - | Telling a preference from a workaround is product judgement. |
| What it leaves behind says whose it is | todo | - | A journey test running the product with a temp HOME could assert every new path under Documents/Desktop/Downloads/~ sits under the product-named folder; project-written. |

### [common/not-now.md](common/not-now.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Write it down in the same commit | todo | - | A lint.d check could match each not-now.md entry's headline to a line in CLAUDE.md's "Not now" list (and fail when a commit body's deferred list adds no not-now.md entry). |
| Fail loudly instead of a silent stub | todo | - | lint should deny clippy::todo/unimplemented (or grep todo!/unimplemented!/throw new Error("TODO")) unless the same or previous line points at not-now.md. |
| Decided "left as it is" is also written down | review | - | Deciding to leave a limitation as it is is judgement; the entry shape is the not-now.md format. |

### [common/privacy-public-repos.md](common/privacy-public-repos.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Made-up names and documentation addresses | partial | check-private refuses listed terms (pre-commit, commit-msg, lint via claude-hook, CI) | Unlisted real hosts/addresses pass: a check should refuse IP literals outside RFC 5737/3849/private/loopback ranges and host names not ending in .example/.internal/.test. |
| Real findings live in a git-ignored local file | partial | check-private refuses a dev/private-terms that git doesn't ignore | Nothing checks `git check-ignore CLAUDE.local.md`; lint should fail when CLAUDE.local.md isn't ignored. |
| A denylist the hooks refuse, failing closed | gate | check-private in pre-commit, commit-msg (check-commit-msg), lint (claude-hook) and CI (actions/rust-lint), fail-closed; tested in tests/run | Gaps: CI skips (with a warning) when the secret is absent, and non-Rust projects have no kit CI workflow running it. |
| People appear as roles | review | - | A person's name can't be told from other words by a script (list known names in private-terms to catch them). |

### [common/releases.md](common/releases.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Only a green main is released | todo | - | No kit release script/workflow (phase 2): the script and the workflow's first job should require `gh run list --workflow ci.yml --commit $SHA --status success` and tag that SHA. |
| One command from Unreleased to the tag | todo | - | No shared release.sh: clean tree equal to origin/main, non-empty Unreleased, kinds only, version set everywhere, resumable; all deterministic. |
| The workflow re-checks, then publishes in safe order | todo | - | No shared release workflow: notes job checks a dated section, version files equal the tag and CI passed; a workflow lint for concurrency release with cancel-in-progress: false. |
| A rehearsal that publishes nothing | todo | - | A workflow lint should require every publishing step in release.yml (gh release create, store uploads) to be gated on github.event_name == 'push'. |
| Slow external steps get honest timeouts | review | - | The limit's multiple and whether the failure message tells slow from refused need judgement (timeout presence is covered by the CI time-limits check). |
| Dependencies: the platform's packages, or bundle and own the updates | review | - | Whether bundled software is provided by the platform's package manager is a packaging judgement. |

### [common/testing.md](common/testing.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Nothing touches the developer's machine | review | - | What a test script could read or change on the machine needs a reviewer. |
| A journey suite is the regression suite | partial | check-coverage runs every cargo test (journey included if it is one) in pre-commit and CI | Nothing checks that a new window/menu item/flag/shortcut adds a journey step, or that the journey runs on every system. |
| One scenario per test, run everywhere | partial | check-coverage sets PRACTICES_SKIP_LOG and prints the skip count and reasons (pre-commit, CI) | A rising skip count fails nothing: a per-system skip baseline (like size-allowlist) should fail when skips rise or fall unrecorded. |
| Failures explain themselves | review | - | Whether a failure message lets you tell what went wrong needs a reader. |
| A step for every IPC call | todo | - | A project guard could list IPC methods from the interface definition (D-Bus XML, proto, enum) and require each to appear in the contract test. |
| Red before green | todo | - | CI could run a PR's added/changed tests against the base commit's non-test code and require them to fail; nothing checks the commit-body line either. |
| No retries for flaky tests | todo | - | A lint.d grep should refuse retry options in workflows and test config (nextest retries, --retries, jest retryTimes, retry actions, rerun-failed). |
| A stuck renderer is asked once more; a failed comparison never is | review | - | Telling a renderer that gave no answer from a comparison that failed needs reading the gate's code; the forced-hang proof is read in the commit. |
| Real-machine bugs become tests | review | - | Linking a person's bug report to its test needs judgement. |
| Fakes refuse what they weren't told | review | - | Whether a fake is permissive is shown by mutating a project's tests; the kit can't detect fakes generically. |
| A guard test per incident, proven able to fail | review | - | Which incidents need a guard is judgement; the self-test is the project's own. |
| Golden fixtures written by the old code | todo | - | A project check that each schema version in code has a fixture with a recorded source commit that exists in history. |
| Two implementations, one known answer | todo | - | A project test that the fallback opens every device-captured vector byte for byte; nothing in the kit. |
| Coverage floors only rise | partial | check-coverage floors (pre-commit on Rust changes, CI rust-coverage refuses a floor lowered against the base) | Only Rust/cargo is covered (no floors for TS/Jest or other languages), and a crate well over its floor is only advised, not failed. |

### [common/voice.md](common/voice.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| The product speaks as itself, never as "we" | partial | check-voice: "we" in English and Czech, in any case (pronouns, jsme/budeme, the -me verb), in string literals, ternary branches, JSX text, JSON, .strings, .xcstrings, .ftl, .po, strings.xml, store text, the changelog, content/, web pages and design boards, each in its language (path, block, element lang, or COPY_LANG) (claude-hook after edits and on Stop, pre-commit, lint); a line marked `practices-allow voice: <reason>` passes, a mark with a reason under three words is a finding | "I" is review (the person's own words use it); an inclusive "we" (a companion and the person together) passes on its mark, and whether it really is inclusive, in a product built as a companion, is review; other languages only through VOICE_WORDS. |
| Each language's grammar is checked | partial | check-copy: each language's rules (copy-rules/<lang>.mjs: cs, en, es, and the project's own) on its own copy, by <html lang>, path or block; copy that names no language, a language without rules, and an exception without a reason are findings; boards and VOICE_FILES (claude-hook after edits and on Stop, pre-commit, lint) | Boards are read as written: text a script writes at load isn't read. Wording that is wrong but not mechanical stays with the reviewer. |

## UI design (ui/)

### [ui/README.md](ui/README.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| What belongs here | partial | tests/readme (kit's own gate, links each ui page from README.md) | Still unchecked: a doc lint that every '## ' rule has What/Why/Apply/Check paragraphs and its Why links or dates an incident. |

### [ui/consent.md](ui/consent.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Two equal answers, no guilt | todo | - | On boards marking the consent pair (data-consent), assert both buttons have equal bounding boxes (within 1 px) and equal text contrast, neither has checked/aria-pressed/aria-selected/selected style on load, the 'no' label matches no guilt pattern list, and a sibling text names what is sent and where to change it (contrast-4.5 only gives the floor, not the equality). |

### [ui/design-before-build.md](ui/design-before-build.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Proposals with options, then build "as chosen" | todo | - | check-commit-msg/pre-commit: a commit touching UI source must name a proposal path or canvas link ('as chosen'), and the proposal page must contain >=2 labelled options and one 'Recommended' marker, with the design doc's Rejected section touched in the same commit. |
| The owner answers one question at a time | review | - | The questions are asked in the agent's dialog, which no script sees; a proposal page's numbered questions could be counted by the proposal-structure check. |
| The design holds only agreed designs | todo | - | check-ui on boards outside proposals/: flag any element with data-variant or text matching 'Option [A-Z]'/'Variant'/'Recommended' unless the page is marked rejected. |
| Keep the design in sync with the code | todo | - | pre-commit: staged UI source with no staged design/board file fails unless the message carries a 'Design: unchanged, <reason>' trailer. |
| A touch-up gets its own before and after | partial | check-commit-msg (commit-msg hook): a commit that changes an existing board (UI_BOARDS) needs a Before-after: trailer naming a page in the repository or an https link, or 'none, <reason>' | A design kept outside the repository (a canvas) isn't seen; a `before-after` script could render the board's crop at HEAD and in the working tree and write the page; whether the page shows one change only is judgement. |
| Read the design's source, never a picture | todo | - | Diff check: every new colour, px/pt length, radius and string literal added to UI source must occur in the design's tokens or board source; unknown literals are listed for the agent. |
| When the agent can't edit the design: a prompt and a sync-back list | todo | - | Markdown lint: every open item in design-sync-back.md references an entry in design-prompts.md whose status is 'sent' or 'returned <date>'. |
| Match one to one, verified by screenshot | todo | - | Render the board and the demo-mode app (for web/RN-web in the same Chrome) at device DPR, crop each data-object, and diff row/column pixel profiles to report line weight, inset and height deltas over 0.5 px. |
| Pixel by pixel: the owner's eye is the bar | partial | check-ui contain, clip (claude-hook, Stop, pre-commit) | Lines, glyphs, the face that renders and the words: compare the built screen's DOM and captures with the board's (fonts via CDP CSS.getPlatformFontsForNode), and each line of text's ink width and left edge, not only the paragraph's box. |
| A screenshot gate launches the app once | todo | - | check-shots could take a dither tolerance (`--dither 2`) and serve as the switch guard; the switch, the ready mark and the settings check are the project's own code. |
| A value the scale doesn't have is a question for the owner | todo | - | check-ui loads the project's scale tokens and flags every computed margin, padding, gap, radius and font-size not on the scale unless data-allow names it as the object's own geometry; a lint.d grep does the same in lint-exempt theme folders. |
| Review a proposal in its place, with fresh eyes | todo | - | Structure check on proposal pages: a section answering the six questions (six non-empty items), a before/after pair, a quoted spec line for each option that changes the spec, and a linked critique record; the critique's quality stays human. |
| Proposal pages pass a checklist before review | partial | check-page sideways, one-letter-end, image-width, image-pixels, doctype, charset, lang (claude-hook, Stop, pre-commit) | A before/after pair taller than 812 px at 375 px, and a page over about 1 MB, are measurable and unchecked; questions beside their images, options drawn fairly and sentences true per screen stay with review. |
| Every fact a screen uses was entered earlier | partial | check-copy fact: every element marked data-fact="KEY" reads the same on every board, per language; a board changed alone is compared with all (claude-hook, Stop, pre-commit, lint) | Whether an earlier step supplies each fact: a click-through test of the prototype could list each data-fact's first screen in flow order and fail when a screen uses one before the step that collects it. |
| Every control records an event or only navigates | todo | - | A check reads every button on the boards (class b-main, b-sub, b-ghost, a sheet's rows) and matches its label to the spec's event table or a `data-nav` mark; a button left over is a finding. |
| Cross each new event with each state before asking | todo | - | In a project with a reference engine, a test enumerates every state and event pair and fails on one the engine doesn't define; whether a round's questions cover the table stays review. |

### [ui/drag-and-drop.md](ui/drag-and-drop.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| One calm panel says what will happen | partial | check-ui contrast, clip, contain (claude-hook, Stop, pre-commit) | One target per kind of drop; the panel covers the window's content. |

### [ui/feedback.md](ui/feedback.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Work shows it's happening | partial | check-ui working: with motion allowed, something inside each element marked aria-busy="true" is animating; check-ui motion: with reduced motion, nothing loops (claude-hook, Stop, pre-commit) | The app's own code is review: whether each wait over a second has its motion, starts and stops with the work, and is the product's own (one motion per screen; a generic spinner isn't detected). A busy state a board draws without aria-busy isn't seen. |
| A press answers at once | partial | check-ui busy: each element marked aria-busy="true" (or the control inside it) is disabled or aria-disabled="true", shows no pointer cursor, and its words end in … (three dots are a finding); check-ui working (claude-hook, Stop, pre-commit) | The app's own code is review: whether each press that starts slow work has its busy state, its shortcut and menu item off, a time limit from the slowest real case, and a journey test that holds the work open, presses again and sees the control return. |
| A placeholder ends | review | - | A UI test that holds the content back (a launch argument) and asserts the message and its retry button appear; a lint that every placeholder view has a deadline (ROADMAP.md). |
| A placeholder is drawn on the page's own edges | partial | check-shots --only-top PX: the loaded page's shot against its placeholder's, over the band above PX, status bar included; run where the project takes its screenshots | Taking the two shots is the project's own script; the side and bottom edges, and a page without such a script: review. |

### [ui/identity-pass.md](ui/identity-pass.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Identity first, before the first screen | todo | - | Doc/git script: the identity brief exists with the six headings (Audience, Job, Inspiration, Market, Idea, Tone) and an agreed date earlier than the first commit of any board. |
| Get the facts right | review | - | Whether a drawing keeps the real thing's identifying features at 16 px is a recognition judgement; at most a script can confirm the mark is shown at its smallest size on a board. |
| The name and the mark read clean (a hard stop) | todo | - | Script generates every cut of the name (prefixes, suffixes, capital/hyphen/line-break splits, truncations, one-letter swaps) and fails unless the brief lists each with a verdict, sources and date; the reading itself stays human. |
| A mark holds at its smallest size | partial | check-ui mark: at the smallest size a board shows each svg[data-mark], from its pixels: strokes 1 px or more, no leftover piece of a cut, the [data-mark-brand] element 10 px or taller, brand touching the letters or a quarter of a stroke clear; a mark never shown at 24 px or less (claude-hook, Stop, pre-commit) | A mark without data-mark isn't measured: nothing yet finds a wordmark that isn't declared. Whether the mark is good is review. |
| The type is chosen for the product, never a tool's default | review | - | Whether a face fits the product is taste; the proposal's blind page and costs are review. The checks below catch what a machine can. |
| Roles by meaning | partial | check-ui tabular: each time (21:05) and each [data-number] element, its figures measured in its own font and settings (ten 0s against ten 1s), after edits, on Stop and in pre-commit | Which face takes which role: a page could declare its roles (meta type-roles, data-role) and check-ui compare; not built. |
| A face change keeps the ink | todo | - | check-ui could compare small text's ink between a board and the board it was derived from (a proposal against the agreed board), within 5 %; nothing does yet. |
| Every face draws the product's own language | partial | check-ui fallback: Chrome's own report of the fonts it drew each element's text in (CSS.getPlatformFontsForNode); a system font under text that asks for a loaded face is a finding, after edits, on Stop and in pre-commit | The spacing around marks (ď, ť) is review. |
| Iteration 1: establish the identity | review | - | The physical idea, its objects' jobs, the trust test and the worst-moment test are judgements; only the presence of a rating and a per-screen verdict list is checkable. |
| Iteration 2: a few parts, shown, iterated, agreed | todo | - | check-ui: one design left per choice (no variant labels on agreed boards), every icon from the family sprite, every third-party asset carries data-source and the board a credit line, embedded SVGs have no script/external href; critique report file exists. |
| Iteration 3: the whole app, re-audited and polished | todo | - | Checklist lint: every inventory line is graded matches/fixed/drifts/not seen, and every 'matches' links an existing capture or board file. |
| An inventory that misses nothing | todo | - | Script: sweep UI source files, routes and i18n string groups and fail on any not mapped to an inventory line; count uses of the shared dialog/sheet/menu/toast/banner by grep and compare with the counts recorded in the checklist; no 'matches' without a picture link. |
| Where the product's mark appears | todo | - | check-ui lists every element using the mark (data-mark or use href to its symbol) per board and fails on boards/states not in the design doc's list of moments; a looping animation on the mark needs data-allow. |
| Before you show anything | partial | check-ui, every check (claude-hook, Stop, pre-commit) | The steps that are process: two reviewers, the capture of every state. |

### [ui/keyboard-shortcuts.md](ui/keyboard-shortcuts.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Bind the system's main modifier, not Ctrl | todo | - | lint.d code scan: flag keymap literals bound to ctrl-/Ctrl+ (GPUI 'ctrl-', Electron 'Ctrl+', web ctrlKey without metaKey) unless allow-listed, and system shortcuts (cmd-h/m/q/w/`) rebound. |
| Show them the way the system writes them | todo | - | check-ui on boards with data-platform: macOS text has no Ctrl/Alt/Cmd/'+' between keys and modifier symbols in order ⌃⌥⇧⌘; Linux/Windows text has no ⌘⌥⌃⇧ and uses Ctrl+Alt+Shift+Key order; the label function's tests stay in the project. |

### [ui/pickers.md](ui/pickers.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Picked, not typed | todo | - | check-ui: flag text inputs/contenteditable and plain text nodes outside a button whose text or placeholder matches date/time/count patterns (\d{1,2}:\d{2}, d. m. yyyy, etc.), and lone toggles whose label is a value; derived-value arithmetic stays a prototype test. |
| Every calendar jumps to a month and year | todo | - | check-ui: each calendar grid (role=grid/data-calendar) has its month title inside a button with a chevron, and a scripted click path reaches a month 36 back in <=4 clicks; disabled months carry aria-disabled. |
| A calendar shows the neighbouring months' days, muted | todo | - | check-ui: every calendar row has 7 non-empty day cells, and in-month, neighbour and disabled cells form three distinct computed-style signatures (background, colour, opacity) with only disabled ones aria-disabled. |
| Suggestions are a starting point, never a fence | todo | - | check-ui: steppers/number inputs with a max and year/option lists without a paging or 'Other' control fail unless data-allow states the real limit; a prototype run at extreme values checks derived text for overflow. |

### [ui/visual-craft.md](ui/visual-craft.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Tone, not outlines | partial | check-ui ring (claude-hook, Stop, pre-commit) | A border census: visible borders and inset rings that aren't focus, a checkbox or marked data-allow; nested cards; floating surfaces without a two-layer shadow. |
| Every stroke end matches | todo | - | check-ui: within each icon family (data-family or sprite), every open SVG path/line has the same computed stroke-linecap and stroke-linejoin; connector elements must precede the marks they meet in paint order. |
| One object, one drawing | todo | - | check-ui: all elements with the same data-object (or use of the same symbol) across boards have the same effective stroke width in screen px (stroke-width x CTM scale), aspect ratio and corner radius. |
| A drawing over an object reaches its edges | todo | - | check-ui: each overlay drawing (data-overlay/svg decoration inside an object) has a bounding rect equal to its parent's border box within 0.5 px, and corner path endpoints land on the parent's corners. |
| A line weight per family | todo | - | check-ui: group strokes by family and fail if one family has more than one effective stroke width or differs from the weight declared in the design tokens. |
| A glyph keeps one ink | partial | check-ui ink: a glyph's stroke and fills (its plane) in one hue, symbols through <use> included (claude-hook, Stop, pre-commit) | A plane under a glyph drawn as a bitmap, and a glyph whose stroke colour comes from a filled shape (an outlined font icon). |
| A drawn icon set, grown from the idea | partial | check-ui icon: every button with words carries an icon, exceptions marked (claude-hook, Stop, pre-commit) | One family: the same stroke width and caps across every icon symbol; list and settings rows. |
| Depth and texture from a concept | partial | check-ui shadow: no zero-offset halo, nothing falling up, offset at least a quarter of the blur (claude-hook, Stop, pre-commit) | One shadow recipe per elevation (data-elevation), light direction from the project's config, raised primaries and pressed selected states, grain where the identity declares texture. |
| The system's own sign for the system's own act | todo | - | check-ui: on boards with data-platform, elements with data-system-act (unlock, share) use that platform's glyph id, and the per-platform glyphs share viewBox and stroke width; the per-platform render test stays in the project. |
| Compact, not breathy | todo | - | check-ui: per screen, distance from header bottom to first content/control top above a threshold (one large scale step) fails, as does empty space between the last content and the board's bottom over a step, unless data-allow. |
| Separate targets keep their distance | gate | check-ui gap: 8 px between targets, across and down; segmented controls (tablist, radiogroup, a group of aria-pressed toggles) need no mark, the other exceptions are marked data-allow; a page behind an open sheet (aria-hidden, inert) isn't measured (claude-hook, Stop, pre-commit) | - |
| Spacing is measured from what you see | partial | check-ui halo: rings of 2 px or more and glows keep 16 px from the ink of text, not its line box; check-ui inset: a filled box over a surface's edge leaves the surface's padding to its text (claude-hook, Stop, pre-commit) | The painted extent of drawings (an SVG's disc behind a mascot) to the text above it. |
| Centred means on the axis | partial | check-ui centre: a centred block more than 3 px off its column's axis (claude-hook, Stop, pre-commit) | A lone centred block among left-aligned siblings. |
| Rank what the screen says | review | - | Which facts a string carries and which leads is semantic; only side checks like abbr/short forms having a full aria-label or title are measurable. |
| A shortcut view says it is a shortcut | review | - | Knowing a list shows part of a range is semantic; once marked data-partial, a heading and a 'whole' link could be structure-checked. |
| A number says what it counts | todo | - | Heuristic in check-ui: a number-with-unit text node within 8 px after a link/button or a label it is not grouped with (no shared parent, no noun) is flagged for the agent; the true reading stays human. |
| One reading only | review | - | Ambiguity of a word or limit is decided only by a reader; regex for 'at most N' or 'N of M' without a subject would be noise. |
| A counting mark keeps one scale | todo | - | check-ui: every element with data-count-unit has the same size and centre-to-centre pitch per unit across all boards. |
| Decoration never half-hides what you read or click | partial | check-ui contrast against the pixels behind text, drawings included; covered text skipped (claude-hook, Stop, pre-commit) | A row or control partly covered by a drawing in front of it (elementsFromPoint across its box). |
| Nothing anyone reads under 11 px | gate | check-ui text-size, SVG text at its drawn size; glyphs in shapes marked data-allow (claude-hook, Stop, pre-commit) | - |
| One anatomy per job | partial | check-ui same-look: like targets (same tag, classes and role; icon buttons apart) share height, type, radius and padding; unclassed ones are asked to name their component (claude-hook, Stop, pre-commit) | Non-target components (toasts, cards) by a declared component name; that the classes match the design doc's component list. |
| A choice changes everything it owns | partial | check-ui state: a focus, hover, active or pressed state never moves or resizes content; same-look (claude-hook, Stop, pre-commit) | Icon colour and dependent fields after a click: a test that clicks each option in a prototype. |
| Show it in real context | todo | - | check-ui: every phone/desktop board contains the shared frame component with a data-source naming its kit, has a distinct dark render, a pseudo-locale variant, and no lorem/placeholder copy. |
| Both safe areas belong to the frame | gate | check-ui safe: in a data-frame="phone", every target ends 34 + 8 px above the bottom (a tab bar 34) and starts below the status bar (54; data-safe-top/-bottom for others), what scrolls is skipped; a frame without its data-home-indicator, and a phone-width board (fixed at 480 px or less) without a frame, are findings (claude-hook, Stop, pre-commit) | - |
| A sheet's page is inert, and the board says so | gate | check-ui sheet: an open dialog (role=dialog/alertdialog, dialog[open]) while a target drawn before it in its screen is live; aria-hidden and inert pages are skipped by every check (claude-hook, Stop, pre-commit) | - |
| Words in the product's voice | partial | check-ui outcome: no button labelled only OK, Yes, No or another word with no outcome; check-copy: each language's mechanical grammar (claude-hook, Stop, pre-commit, lint) | check-ui: dialog body <=2 line boxes; boards mentioning a person present each gender variant; tone and jokes stay human (review). |
| Answer the next question where it arises | review | - | What the user will ask next is semantic; only 'every failed/error state has a next-action button' is a structure check. |
| Motion with a reason | partial | check-ui motion: every board is rendered with reduced motion (every check measures that render), and an infinite animation still running there is a finding unless marked data-allow (claude-hook, Stop, pre-commit) | Finite animations and transitions that still play with reduced motion, SVG <animate> loops, and generic spinners (known spinner classes, a rotating circle); whether a motion tells the product's story is review. |
| A selection switches at once | partial | check-motion: in Swift (MOTION_FILES), a selection state (selected…, selection…, highlighted…, …Selection, …Selected, plus MOTION_SELECTION) set inside withAnimation or followed by .animation(_:value:); practices-allow motion with a reason of three words or more (lint, claude-hook, Stop, pre-commit) | Kotlin and Compose (animate*AsState on a selection), the web (a CSS transition on a selected class), a highlight under another name, and an animation set by a parent's transaction: review. |
| A resize never shows a squashed frame | partial | check-ui squash: an element holding words drawn scaled out of its shape, or playing a @keyframes rule (under any media) that scales it so; data-allow for a deliberate one (claude-hook, Stop, pre-commit) | A uniform scale (a popover's scale-in), transitions to a scaled state, and the native app's own window resize: review, by recording the resize frame by frame. |
| Nothing runs past its surface | gate | check-ui contain and clip, at every width and theme (claude-hook, Stop, pre-commit) | - |
| A button label stays on one line | gate | check-ui wrap: the text of a button, tab, radio, switch or menu item never runs onto a second line, unless it sits in a flex column inside the target (claude-hook, Stop, pre-commit) | - |
| Buttons follow the column | partial | check-ui align: a row of buttons starts at its column's leading edge, fills it, or is centred in a centred column; a lone button may sit at the trailing edge; a lone button never stretches across a surface wider than 480 px (claude-hook, Stop, pre-commit) | Whether a lone trailing button moves on (its wording) is review; equal widths in a full-width row aren't checked. |
| Every button names its outcome | partial | check-ui outcome: no button whose accessible name is only a word that names no outcome, from the vagueButtons of the language it is in (copy-rules/<lang>.mjs: Cancel, OK, Yes, No, Zrušit, Ano, Cancelar…) (claude-hook, Stop, pre-commit) | Whether a specific label says the outcome ("Keep the app" beside "Remove") is review. |

### [ui/window-buttons.md](ui/window-buttons.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| macOS draws its own buttons; the header makes room | todo | - | check-ui on macOS boards: no app close/min/max in the header, first header item starts at or after the reserved 96 px, title's vertical middle within 1 px of the buttons' middle, gap after the green button equals the gap before the red. |

## Rust (rust/)

### [rust/conventions.md](rust/conventions.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| One workspace, set once | todo | - | Nothing checks Cargo.toml: a lint step (cargo metadata/toml parse) should fail unless resolver=3, edition 2024, publish=false via [workspace.package] inherited by every member, and every member dependency is `.workspace = true` or a path (no version strings); run in lint (claude-hook, pre-commit, CI); the per-dependency why-comment stays review. |
| Unsafe code in one crate | partial | check-unsafe in lint (claude-hook, pre-commit, CI rust-lint) | Not checked: `#![forbid(unsafe_code)]` in every crate root outside UNSAFE_ALLOWED (grep lib.rs/main.rs) and `// SAFETY:` comments (clippy::undocumented_unsafe_blocks, not in clippy::all, add to Cargo-lints.toml); also the doc says UNSAFE_PATHS but lib.sh/check-unsafe read UNSAFE_ALLOWED, so following the doc allows nothing. |
| OS code behind small modules | todo | - | A lint step could fail on `#[cfg(target_os` / `cfg!(target_os` outside `**/sys/**` with a shrink-only allowlist, and on OS-only crates outside [target.'cfg(...)'.dependencies]; rust-ci has no `cargo check --target x86_64-pc-windows-gnu` input; stub quality stays review. |
| Errors are sentences | review | - | Whether a message reads as a finished sentence a user understands is a wording judgement. |
| Logs to stderr | todo | - | A grep in lint could require every `tracing_subscriber::fmt()` init to set `.with_writer(std::io::stderr)` and an `is_terminal` ANSI switch, plus clippy::print_stdout in non-CLI crates; the kit checks none of it. |
| Config refuses what it doesn't know | todo | - | A lint step could fail on any `#[derive(..Deserialize..)]` struct in config modules without `#[serde(deny_unknown_fields)]` (allowlist for wire types); the prose test is project-written. |
| Small files and functions | partial | check-size and clippy::too_many_lines in lint (claude-hook, pre-commit, CI) | The `//!` first line per module is unchecked (grep: first non-blank line of each .rs starts with `//!`), and too_many_lines (pedantic) only fires if the project pasted Cargo-lints.toml, which nothing verifies. |
| Magic numbers have names | todo | - | The kit ships no literal linter (Crake's lint-literals is project-local in lint.d); ship it as a lint step that fails on numeric literals other than 0/1/2 outside const/static/enum/tests without `// literal:`. |
| Windows: the C runtime linked in | todo | - | Lint could grep .cargo/config.toml for `+crt-static` on both *-pc-windows-msvc targets, and a kit Windows CI job could fail when a built .exe contains `VCRUNTIME140`; the kit has neither. |
| Measure before claiming numbers | todo | - | check-commit-msg could refuse a message matching faster/speed up/quicker/perf with no number and unit (ms, %, fps, s) in it; soundness of the measurement stays review. |

### [rust/coverage.md](rust/coverage.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| A floor per crate, per OS | partial | check-coverage (pre-commit when .rs staged; CI rust-coverage) | A workspace member with no line in .practices/coverage-floors is never measured; compare `cargo metadata` workspace members with the floors file and fail on a missing crate. |
| Never lowered | partial | check-coverage with PRACTICES_BASE_REF (CI rust-coverage only) | The awk only compares crates still in the new file, so deleting a crate's line (or a new branch's first push, which has no base) escapes; also report crates present in the base but gone from the head. |
| Under the floor, say where | gate | check-coverage prints missing lines (pre-commit, CI rust-coverage) | - |
| Test-harness code stays out of the share | review | - | Whether a path is really harness code and not app code is a judgement on each COVERAGE_EXCLUDE change. |
| One instrumented build runs everything | gate | check-coverage (llvm-cov show-env, extra scripts in the same build); rust-ci.yml single check job | - |

### [rust/gpui.md](rust/gpui.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Dev profile: optimise a little | todo | - | In GPUI projects lint could check Cargo.toml has [profile.dev] opt-level=1 and [profile.dev.package."*"] opt-level=2 (toml parse); the frame-budget part needs a measurement. |
| Headless window tests | todo | - | A lint step could fail when gpui's `test-support` feature appears outside [dev-dependencies] (cargo metadata) and when a module defining a window view (impl Render + open fn) has no sibling tests.rs; nothing in the kit checks it. |
| The journey kit | todo | - | rust-ci.yml runs on one runner (runs-on input), so "journey on every system" needs an OS matrix input running the journey test on Linux, macOS and Windows. |
| Demo, show and appearance switches | todo | - | A kit lint.d/CI step could run the app with each `<APP>_SHOW/_DEMO/_APPEARANCE/_MOTION=nonsense` and require a non-zero exit listing the valid values; not shipped. |
| Frame timing | todo | - | Only presence is machine-checkable (grep for an `<APP>_BENCH` switch in GPUI projects) and the "faster commit quotes medians" heuristic belongs in check-commit-msg; low value. |
| Window buttons on macOS | todo | - | A grep in lint could fail on any `TitlebarOptions` with `appears_transparent: true` that lacks `traffic_light_position: chrome::traffic_lights()`; the per-window title test is project-written. |
| Keyboard shortcuts per system | todo | - | A grep in lint could refuse `KeyBinding::new("ctrl-` (use `secondary-`) and modifier names (Ctrl, Cmd, Alt, Option, the symbols) in locale/.ftl files; both checks in the doc are project-written tests. |
| Rounded corners don't clip | partial | check-gpui-clip in lint, in a GPUI app (claude-hook, pre-commit, CI rust-lint): an element that rounds and clips in one builder chain, a one-parameter closure on the element included; `// practices-allow clip:` with a reason of three words or more | An element built over several statements through a variable, or rounded in a helper and clipped by its caller; whether each corner child carries the parent's radius minus its border is review (the app at 2×). |
| CI packages for GPUI on Linux | gate | actions/rust-setup with gpui: true (rust-ci.yml, CI); a missing package fails the build | - |
| Dependabot leaves GPUI alone | todo | - | The template's ignore list is commented out and lacks gpui-fast*; lint could fail in GPUI projects when .github/dependabot.yml's cargo entry doesn't ignore gpui-kit*, gpui-pre* and gpui-fast*. |
| Keeping a patched GPUI current | todo | - | The Cargo.lock check is Crake's own; the kit could fail lint whenever Cargo.lock has a `[[patch.unused]]` section (an unapplied [patch]), and ship the weekly update workflow. |

### [rust/lints.md](rust/lints.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Lints denied in the workspace | partial | cargo clippy --workspace --all-targets in lint (claude-hook, pre-commit, CI) | lint runs clippy without `-D warnings` and nothing checks Cargo.toml has [workspace.lints] or every member `[lints] workspace = true`, so a project without them passes with warnings; `#[allow` is not refused (add clippy::allow_attributes and allow_attributes_without_reason = deny to Cargo-lints.toml). |
| Pin the toolchain | partial | rust-toolchain.toml honoured by rustup and actions/rust-setup; rust-toolchain-bump.yml (if called) | Nothing fails when rust-toolchain.toml is missing or its channel isn't an exact x.y.z (lint check), or when the project doesn't call rust-toolchain-bump.yml. |
| Lint for every target OS | todo | - | lint and rust-ci run clippy for the host only; rust-ci needs a clippy-targets input running `cargo clippy --workspace --all-targets --target x86_64-pc-windows-gnu` (rust-setup already takes targets) and a macOS job. |
| cargo deny: advisories, licences, sources | partial | cargo deny check in lint (claude-hook, pre-commit, CI rust-lint); rust-advisories.yml | Nothing checks the project's workflows call rust-advisories.yml daily (grep .github/workflows); the changelog/hotfix part for a security fix is review. |
| cargo machete: no unused dependencies | gate | cargo machete in lint (claude-hook, pre-commit, CI rust-lint) | - |
| Size limits | partial | check-size and clippy too_many_lines in lint (claude-hook, pre-commit, CI) | File sizes are gated; the 200-line function limit depends on the project having pasted `too_many_lines = "deny"` and clippy.toml, which nothing verifies (pass `-D clippy::too_many_lines` in lint or check Cargo.toml). |
| Unsafe in one place | gate | check-unsafe in lint (claude-hook, pre-commit, CI rust-lint) | Doc names UNSAFE_PATHS but the script reads UNSAFE_ALLOWED; fix the doc. |
| Project-specific steps | partial | lint runs .practices/lint.d/* (claude-hook, pre-commit, CI) | lint silently skips a lint.d file that isn't executable; it should fail on any non-executable regular file there. |
| Where the gate runs | partial | install-hooks --check in lint (local); claude-hook; pre-commit; commit-msg; rust-ci | Git hooks are verified, but nothing checks .claude/settings.json registers claude-hook (copied only with --templates) or that the project's CI calls rust-ci.yml; pre-commit is skippable with --no-verify, so CI wiring is the real backstop. |

## TypeScript (typescript/)

### [typescript/conventions.md](typescript/conventions.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Braces around every body | todo | - | The kit ships no ESLint config; ship a shared flat config with `curly: ['error', 'all']` that the project's `lint` script (NPM_CHECKS) runs. |
| Strict types, and every escape counted | partial | tsc --noEmit in lint (claude-hook, pre-commit) | Nothing checks `tsc --showConfig` has strict, noUncheckedIndexedAccess and forceConsistentCasingInFileNames true, or that each any/@ts-expect-error has a reason (@typescript-eslint/no-explicit-any, ban-ts-comment allow-with-description). |
| Errors are typed codes; the UI picks the words | review | - | Whether a string is user-facing and whether each flow offers a retry needs reading the flow. |
| No direct console calls in the app | todo | - | ESLint `no-console: error` for src/ with the logger file excepted (or a grep `console\.` in src outside the logger in lint); not shipped. |
| Heavy modules load lazily, with `require` | todo | - | Lint could grep `import(` in src (or ESLint no-restricted-syntax on ImportExpression) and fail; which modules count as heavy stays review. |
| Every disabled lint rule has a counted reason | todo | - | Ship @eslint-community/eslint-comments/require-description, run ESLint with --max-warnings 0, and fail when `eslint --print-config` has any rule at severity warn/1. |
| Platform code behind an interface, with a test double | todo | - | ESLint no-restricted-imports / import/no-restricted-paths forbidding services/ from importing screens/ and app/ (paths in project config); not shipped. |
| Patched dependencies: why, when to remove, pinned exactly | todo | - | A lint step (jq on package.json) could fail when a patches/<pkg>+<ver>.patch package isn't pinned exactly to <ver>, postinstall lacks `patch-package --error-on-fail`, or docs/engineering has no row for <pkg>. |

### [typescript/lints.md](typescript/lints.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| The gate: tsc and ESLint, errors only | partial | tsc --noEmit and NPM_CHECKS in lint (claude-hook, pre-commit) | ESLint runs only if the project's own `lint` script calls it, --max-warnings 0 isn't enforced, and the kit ships no TypeScript CI workflow (only rust-ci), so nothing runs it in CI. |
| How `.practices/bin/lint` runs it | gate | lint (tsc, NPM_CHECKS) via claude-hook and pre-commit; pre-commit runs NPM_TEST | tsc is skipped silently without tsconfig.json, and there is no kit CI for JS/TS. |
| The gate visits every file | todo | - | Compare ESLint's linted files (`eslint --format json .` filePaths) with lib.sh js_files and fail on any tracked .ts/.tsx/.js/.mjs/.cjs not linted; run in lint. |
| No two names that differ only by case | todo | - | Add `git ls-files \| tr A-Z a-z \| sort \| uniq -d` (non-empty fails) to lint for every project, plus forceConsistentCasingInFileNames via tsc --showConfig. |
| Size limits | gate | check-size over js_files in lint (claude-hook, pre-commit) | No kit CI for JS/TS projects. |

### [typescript/testing.md](typescript/testing.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Native modules faked as in-memory stores | review | - | Whether a mock behaves like a tiny real module is a fidelity judgement. |
| Fakes refuse what they weren't told | review | - | How each fake handles unconfigured calls is design inside project test code, not a pattern a script can recognise. |
| No real network in tests | todo | - | Kit could ship a Jest setup file (or check that a setupFiles entry from `jest --showConfig` assigns a throwing global.fetch) and a canary test calling fetch that must fail. |
| Jest sees only the project's tests | todo | - | Lint could fail when `npx jest --listTests` lists any path under .claude/ or build/native folders, or when `jest --showConfig` moduleFileExtensions doesn't end in json. |
| Dev scripts are tested too | todo | - | Lint could fail when a file under scripts/ has no matching *.test.* file (by basename). |
| A timeout is not a fix for slowness | todo | - | Fail when `jest --showConfig` testTimeout exceeds 5000 or setup calls jest.setTimeout, and when pre-commit's NPM_TEST output contains "failed to exit gracefully" / open-handle warnings. |
| Coverage: measure, then set floors | todo | - | The kit runs no JS coverage: require coverageThreshold in jest config, run tests with --coverage in pre-commit/CI, and refuse lowered thresholds against the base ref like check-coverage. |

## Mobile apps (mobile/)

### [mobile/app-review.md](mobile/app-review.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Every rejection becomes a practice and a check before the resubmission | review | - | Whether a rejection's fix came with its rule and its check needs a person reading the resubmission's commits. |
| Every binary carries the entitlements its frameworks need | partial | check-xcode (lint, claude-hook after edits and on Stop, pre-commit): each shipped target's imports and linked frameworks against its entitlements file; check-ios-artefact (claude-hook after the agent's `xcodebuild archive` or `-exportArchive`, and before the agent's upload: `-exportArchive` to `upload`, `altool --upload-app`/`--upload-package`, `iTMSTransporter -m upload`): each bundle's `otool -L`, through embedded frameworks, against its signature | An upload by hand, by CI or by fastlane isn't checked (phase 2's release script); the table knows five frameworks for certain, the rest need ENTITLED_FRAMEWORKS. |
| The app is built for the devices it declares | gate | check-xcode: TARGETED_DEVICE_FAMILY of each shipped target, per configuration, against DEVICE_FAMILY or the project level (lint, claude-hook, pre-commit); check-ios-artefact: UIDeviceFamily of each bundle | - |
| A button that leads to a permission prompt says Continue | partial | check-permission-words (lint, claude-hook after edits and on Stop, pre-commit): a grant verb and a permission as a whole string, anywhere; a bare grant verb in a file that asks the OS for a permission | A bare "Allow" in a view whose permission request is in another file isn't found; languages past en, cs, es and vi need PERMISSION_VERBS and PERMISSION_NOUNS; whether other words lead to a prompt, and the Settings link after a refusal, are review. |
| Every screen fits a small iPhone at a large text size | partial | check-ui-tests (lint, claude-hook, pre-commit): a test run names an iPhone SE simulator and sets a large text size | That the run happens (no kit iOS CI), that every screen is reached with its main button asserted on screen, and dark mode, aren't checked. |
| Xcode's accessibility audit runs on every screen, the first-run ones too | partial | check-ui-tests: some UI test calls performAccessibilityAudit | Which screens are audited: a list of the app's screens checked against the audited ones would close it. |
| UI tests pin the app's language | partial | check-ui-tests: each Swift file that launches XCUIApplication() names a UITEST_LANGUAGE argument | Espresso, Detox and Maestro tests aren't read. |

### [mobile/ci.md](mobile/ci.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Public: every platform on every push. Private: before every release | todo | - | No kit mobile CI workflow: a reusable one should build iOS/Android on push (public) and a release check should require a green iOS and Android build on the tagged commit. |
| A compile check: device SDK, Debug, unsigned | todo | - | A reusable mobile workflow with xcodebuild -destination generic/platform=iOS Debug CODE_SIGNING_ALLOWED=NO, plus a workflow lint that the iOS job's env holds no secrets. |
| Pin the runner image and Xcode, with the reason | todo | - | A workflow lint should refuse macos-latest for mobile jobs and require DEVELOPER_DIR defined exactly once with a comment (one grep). |
| Toolchains come from the project's own files | todo | - | A workflow lint should refuse literal go-version/node-version/java-version/NDK versions when go.mod/.nvmrc/engines/build.gradle name them, and any @latest tool install. |
| The local gate builds every platform before a tag | todo | - | The kit ships no release script: it should run xcodebuild and ./gradlew assembleRelease plus the artefact check before tagging and stop on failure. |
| A build made as a check publishes nothing | todo | - | Check scripts should export SENTRY_DISABLE_AUTO_UPLOAD=true (lint.d grep) and fail when their build log contains upload lines. |

### [mobile/devices.md](mobile/devices.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Never test on a device that holds real data | todo | - | A PreToolUse Bash hook should refuse adb/emulator/simctl wipe, reset or test commands that name a device outside a DEMO_DEVICES list in .practices/config. |
| The service's test environment, never production | partial | check-private refuses test-account IDs, but only if the project lists them in dev/private-terms | Nothing requires the IDs to be listed or that test passwords come from env; the test-account banner and per-account environment are project tests. |
| A feature is done once it is walked on a device | review | - | A device walk is done by a person. |
| A live switch draws what a fresh start draws | partial | check-shots: two shots of each screen, fresh and live, compared pixel for pixel outside the status bar | Shooting the screens needs the project's own walk (adb, simctl); nothing runs it on its own. |
| A crash report from the field becomes a test | review | - | Linking a crash-report issue to its test needs judgement. |
| Expected refusals from the OS aren't reported | todo | - | A project test per refusal code plus one other code still reported; nothing in the kit. |
| Config that native tools rewrite is held by tests | todo | - | The kit could ship a lint.d check for known keys (ITSAppUsesNonExemptEncryption in Info.plist, allowBackup with dataExtractionRules); otherwise project tests. |

### [mobile/lifecycle.md](mobile/lifecycle.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| Modals close when the app goes to the background | todo | - | An eslint rule or lint.d grep requiring every Modal/Sheet/Dialog to use useCloseOnBackground; the app-switcher look stays a walk. |
| The privacy cover lives where the OS calls it | todo | - | A lint.d check that the SceneDelegate implements sceneWillResignActive and sceneDidBecomeActive when Info.plist declares a scene manifest; the walk after Xcode upgrades stays human. |
| An action with no idempotency key runs once | review | - | Which actions the server can't de-duplicate is domain knowledge; the double-call test is project-written. |
| Explain before the permission prompt, and ask once | partial | check-permission-words: the button before the prompt says Continue, never "Turn on" or "Allow" (lint, claude-hook, pre-commit) | Whether the explanation is clear and asked at the right moment needs a person; "no prompt at launch" is mechanical and unchecked. |
| A cold-start tap is queued, not lost | todo | - | A device e2e flow (kill the app, open a notification/link, assert the screen) run before releases; nothing in the kit. |
| No layout jumps | review | - | Seeing that nothing moves while a screen loads needs a person watching it. |
| The largest text size and Reduce Motion | partial | check-ui-tests: an iOS project's UI test run sets a large text size on an iPhone SE simulator | Still mechanical and unchecked: render tests at the largest font scale, a lint for fixed height on text containers and for animations not reading useReducedMotion, and a 44 pt touch-target check; the walk stays human. |
| Text takes its container's width | review | - | The doc says only an Android walk proves it; a clipped last word needs a person reading the device screen. |
| Every string names its face, checked on Android | todo | - | An eslint no-restricted-imports rule could refuse the UI kit's Button/Input/Text outside the theme module; the Android letter-shape comparison stays review. |
| A control fades as one piece | todo | - | A lint could flag opacity on a container with children lacking needsOffscreenAlphaCompositing; the colour match on Android stays review. |
| The first screen never waits on the network | partial | check-ui-tests: some Swift UI test file matches UITEST_OFFLINE (default: a launch argument ending in Offline) (lint, claude-hook, Stop, pre-commit) | That the app honours it (every request of its own fails at once), that the test asserts the first screen's content, request timeouts, and Espresso, Detox and Maestro tests: review. |

### [mobile/releases.md](mobile/releases.md)

| Rule | Status | Enforced by | Still to check |
| --- | --- | --- | --- |
| The version comes from the tag; native files are never edited | todo | - | No kit check: CI should refuse version edits in ios/*.xcodeproj and android/app/build.gradle (placeholders 1.0/1) and the release workflow should refuse a tag that disagrees with package.json. |
| Build numbers come from the CI run | todo | - | A workflow lint should require build numbers from github.run_number (Android run_number*100+run_attempt) and a comment next to the workflow's name. |
| Another build of the same version: `+N` | todo | - | The release script should check every tag it made is in `git ls-remote --tags origin` before computing +N. |
| Release uploads are never cancelled | todo | - | A workflow lint should refuse cancel-in-progress: true in the release workflow (one grep). |
| A store whose secrets are missing is skipped, by name | todo | - | A workflow lint should require `if: steps.ready.outputs.ready == 'true'` on every upload step of each store job. |
| Signing in a throwaway keychain | todo | - | A workflow lint should require an if: always() cleanup step deleting the keychain/keystore whenever security create-keychain or a keystore decode appears. |
| Check the artefact before the store sees it | partial | check-ios-artefact: an .ipa or .xcarchive's device families and each binary's entitlements (claude-hook after the agent archives) | Bitcode (otool -l \| grep __LLVM), per-architecture native symbols, Android .aab files, and a release workflow that runs it before upload. |
| Store notes come from the changelog, limits checked after folding | todo | - | The release script should count each language's final notes (Play 500, Apple 4,000) after folding and stop before tagging. |
| Every release goes to TestFlight testers; promotion is by hand | todo | - | A workflow lint should refuse any step that submits for App Review or promotes on Play; the owner's phone use stays human. |
| Google Play: the first release is manual | review | - | The Play listing's state is a fact a person records from the Play Console. |
