# Rust: GPUI desktop apps

What applies to apps built on GPUI (directly or through `gpui-kit`): build profiles that keep frames smooth in development, headless window tests, a journey suite that drives the real app shell, a demo mode, CI packages, and how to keep a patched GPUI current.

Links point at commits in [Crake](https://github.com/dorhawk-software/crake).

## Dev profile: optimise a little

**What.** In development builds, the app's own code builds at opt-level 1 and its dependencies at opt-level 2.

**Why.** Unoptimised GPUI stutters. In tern, building the inbox's elements took about 40 ms a frame, and animations ran at about 20 fps.

**Apply.**
```toml
[profile.dev]
opt-level = 1

[profile.dev.package."*"]
opt-level = 2
```
For headless test binaries in CI, `CARGO_PROFILE_DEV_OPT_LEVEL=0` builds faster, and nothing needs to look smooth there ([8bab495](https://github.com/dorhawk-software/crake/commit/8bab495)).

**Check.** Frame timing (below) in a dev build stays under the frame budget.

## Headless window tests

**What.**
- Every window has a `tests.rs` using `#[gpui_kit::test]` and the test-window helpers (click, type, press, scroll).
- An element is clickable in tests once `.test_support()` is its last call. Without the dev feature, that call does nothing.
- GPUI's `test-support` feature is on only in dev-dependencies.

**Why.** Every window in Crake got tests on the first day ([20a738b](https://github.com/dorhawk-software/crake/commit/20a738b), [6beb084](https://github.com/dorhawk-software/crake/commit/6beb084)). It has 153 `.test_support()` calls.

**Apply.**
- Tests that do real I/O call `cx.executor().allow_parking()`.
- Nothing of the machine leaks in: fixed discovery results, and prefs in a scratch mode that writes nothing.
- Tests see no monitors ([1ba22e2](https://github.com/dorhawk-software/crake/commit/1ba22e2)).

**Check.** A review question for a new window: where is its `tests.rs`?

## The journey kit

**What.** `main()` is `start(cx, Setup)`. The journey suite runs that real app shell on GPUI's headless test platform, through a small kit:
- `until(cx, what, deadline, pred)`
- `click(id)`
- `type_into(id, text)`
- `wait_window::<V>()`
- `settle()`

**Why.** See [common/testing.md](../common/testing.md#a-journey-suite-is-the-regression-suite) ([7a28ba2](https://github.com/dorhawk-software/crake/commit/7a28ba2)). The test platform never sends the next frame or resize events by itself, so `settle()` draws frames by hand and calls `simulate_window_resize`. Windows that fit their content need a fixed tall size in tests.

**Apply.**
- Copy the kit from Crake's `journey_kit.rs` until it is published (planned as a crate, or an addition to gpui-kit).
- `<APP>_JOURNEY_DEBUG=1` prints each click target's bounds and whether it is visible.

**Check.** CI runs the journey on every system.

## Demo, show and appearance switches

**What.** Environment variables make the app show the design's sample data, open a given window, and pin the appearance:
- `<APP>_DEMO=<variant>`: sample data, with no network, keyring or daemon.
- `<APP>_SHOW=<window>[:<arg>]`: open that window at start.
- `<APP>_APPEARANCE=light|dark`.
- `<APP>_MOTION=slow|off`.
- A pseudo locale.

Each variable is parsed once, into an enum that refuses unknown values with the list of valid ones.

**Why.**
- They let the app be compared side by side with the design's mockups, and filmed.
- In Crake they grew as scattered string matches in `main.rs`. An unknown value silently fell back, and nothing listed them.

**Apply.**
```rust
enum Show { Settings, Log, Detail(String) }
impl FromStr for Show { /* "settings" | "log" | "detail:<x>" ; else Err(list of valid values) */ }
```
Keep a table of the variables in the project's docs.

**Check.** `<APP>_SHOW=nonsense` exits with the list of valid values.

## Frame timing

**What.** A switch prints frame timings, so performance claims come from measurements.

**Why.** tern's `TERN_BENCH=1` (with `ZED_MEASUREMENTS=1`) is the template. Runs vary by about ±30%, so compare medians of several runs. Use a frame-pointer build for `perf`.

**Apply.** Add `<APP>_BENCH=1`, which logs build, layout and paint time per frame and a summary on exit. Document how to profile.

**Check.** A "faster" commit quotes before and after medians.

## CI packages for GPUI on Linux

**What.** GPUI links X11, Wayland, keyboard, font and Vulkan libraries.

**Apply.** `actions/rust-setup` with `gpui: true` installs:
```text
build-essential pkg-config cmake clang
libxcb1-dev libxkbcommon-dev libxkbcommon-x11-dev libwayland-dev
libfontconfig-dev libfreetype-dev libvulkan-dev
```
A real window in CI runs on Xvfb with Mesa's lavapipe in a container with no network ([ca48892](https://github.com/dorhawk-software/crake/commit/ca48892), [900f0b9](https://github.com/dorhawk-software/crake/commit/900f0b9)).

**Check.** The CI job builds with no other apt step.

## Dependabot leaves GPUI alone

**What.** Dependabot ignores `gpui-kit*`, `gpui-pre*` and `gpui-fast*`. GPUI moves together with its patch and the app's API changes, by hand or by the update bot.

**Why.** A grouped bump can quietly drop a vendored patch. GPUI updates also break APIs, as GPUI 0.9's scroll rename did ([01ff76e](https://github.com/dorhawk-software/crake/commit/01ff76e)).

**Apply.** It's in [templates/dependabot.yml](templates/dependabot.yml) as an ignore list.

**Check.** No Dependabot pull request touches GPUI.

## Keeping a patched GPUI current

**What.** When the app needs a change GPUI doesn't have yet:
- The patched crate is vendored and wired in with `[patch.crates-io]`.
- A `.patch` file holds the canonical diff, and a `*-PATCH.md` explains each change.
- An update script re-applies the patch to the newest GPUI each week. If the patch applies in reverse, upstream has taken it, so the vendored copy is dropped.
- A weekly workflow opens a pull request, or an issue when the patch no longer applies.
- A lint step fails if Cargo.lock doesn't use the patched copy.

**Why.** A `[patch]` that no longer matches is only a Cargo warning. The unpatched crate would ship with every test green ([6b0026c](https://github.com/dorhawk-software/crake/commit/6b0026c)). A pull request opened with `GITHUB_TOKEN` doesn't start CI, so the workflow dispatches CI on the branch itself.

**Apply.**
- Copy Crake's `scripts/update-gpui.sh`, `scripts/check-gpui-patch.sh` and `.github/workflows/gpui.yml` (to be generalised in a later phase).
- Put the check in `.practices/lint.d/`.
- Offer the change upstream.

**Check.** The lint step, plus the weekly workflow's pull request or issue.
