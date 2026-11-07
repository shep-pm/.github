<!-- Two parts. The first is for people reviewing this. The second is for the
coding agents and scripts that also read pull requests. Delete any line that
does not apply. -->

## What this changes

<!-- A few bullets. What is different after this merges, not how you got there. -->

-

Resolves #

## Precise details

<!-- Exact rather than readable. Repo-relative paths only. -->

- Surface changed: <!-- command, flag, setting, JSON field, exit code, default; or none -->
- Breaking: <!-- what breaks for a user, and the commit marked `!`; or no -->
- Not tested: <!-- platforms, paths and cases you did not run -->

## Before you ask for review

- [ ] Every commit subject is a conventional one, `type(scope): summary`, with `!` on the commit that breaks something. release-plz builds the changelog and the version from them and drops what it cannot parse.
- [ ] `cargo fmt --all --check`, `cargo clippy --all-targets -- -D warnings`, and the tests for what you changed pass. CI runs the full suite.
- [ ] I can explain every line of this. Using an AI to write it is fine and common here. Opening a pull request you cannot answer questions about is not, whoever or whatever wrote it.
