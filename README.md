# .github

Org-level files for [shep-pm](https://github.com/shep-pm).

- `profile/README.md` is what renders at <https://github.com/shep-pm>.
- `profile/assets/` holds its artwork. `generate.py` draws the banner and the
  flock map, one file per colour theme, and `<picture>` picks between them.
  `terminal.svg` is a copy of `assets/hero.svg` from the shep repo.

Regenerate the artwork after editing `generate.py`:

```bash
python3 profile/assets/generate.py
```

Colours come from `web/src/styles/tokens.css` in
[shep-pm/shep](https://github.com/shep-pm/shep), so the page matches
[shep-pm.com](https://shep-pm.com).
