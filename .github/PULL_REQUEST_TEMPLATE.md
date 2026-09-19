<!-- Two parts. The first is for people reviewing this. The second is for the
coding agents and scripts that also read pull requests. Delete any line that
does not apply. -->

## What this changes

<!-- A few bullets. What is different after this merges, not how you got there. -->

-

Closes #

## Precise details

<!-- Exact rather than readable. Repo-relative paths only. -->

```
crates touched:
public API change:
new or changed surface: (verb, flag, Flockfile key, JSON field, exit code, default)
docs updated:
```

## Before you ask for review

- [ ] I can explain every line of this. Using an AI to write it is fine and common here. Opening a pull request you cannot answer questions about is not, whoever or whatever wrote it.
- [ ] Every commit subject is a conventional one, `type(scope): summary`. release-plz reads individual commits and silently drops what it cannot parse, so an unreadable subject contributes nothing to the changelog and nothing to the version bump. Accepted types: `feat`, `fix`, `perf`, `refactor`, `docs`, `test`, `ci`, `chore`, `style`.
- [ ] Anything that breaks a caller carries a `!`, on the commit that breaks it, in the crate that breaks. A `!` on this title is read by nobody.
- [ ] `cargo fmt --all --check`
- [ ] `cargo clippy --workspace --all-targets --all-features -- -D warnings`
- [ ] `cargo test --workspace --all-features`
- [ ] If this changes anything an operator types or sees, `web/` says so too. Regenerate with `./web/scripts/generate-cli-reference.sh`, then read the hand-written pages under `web/src/pages/docs/`, then run `npm ci && npx astro check && npm run build` from `web/`.
