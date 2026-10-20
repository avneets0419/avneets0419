# Maintaining this profile

This repository powers the README shown on [github.com/avneets0419](https://github.com/avneets0419).
GitHub renders `README.md` from the default branch (`main`) of a public repository whose name matches the username.

## Layout

```
README.md                      profile page
assets/hero/                   animated hero + typing line, with static (reduced-motion) versions
assets/projects/               one pipeline card per featured repository
assets/ui/                     section divider and link buttons
scripts/generate_assets.py     source of every SVG in assets/ (Python 3.9+, standard library only)
.github/workflows/snake.yml    daily contribution-snake job
```

## Editing the custom visuals

All SVGs in `assets/` are generated. Edit the content constants or layout code in
`scripts/generate_assets.py` (name, tagline, terminal lines, typing phrases, project cards), then run:

```bash
python3 scripts/generate_assets.py
```

The SVGs are self-contained: no JavaScript, no external fonts or stylesheets (system font stacks only).
Animation uses CSS keyframes and SMIL, both of which work inside GitHub's `<img>` rendering. CSS
animations stop for visitors who prefer reduced motion, and the README serves the `*-static.svg`
versions of the hero and typing line to them via `<picture>`.

## Contribution snake

`.github/workflows/snake.yml` runs [Platane/snk](https://github.com/Platane/snk) (pinned to the v3.5.0
commit SHA) every day at 02:23 UTC and on manual dispatch. It writes `snake-dark.svg` and `snake-light.svg`
to the `output` branch and only commits when the files changed. The README loads them from
`raw.githubusercontent.com/avneets0419/avneets0419/output/`.

One-time setup after the first push:

1. Repository **Settings → Actions → General → Workflow permissions**: the workflow requests
   `contents: write` itself, but if the organization/account policy forces read-only tokens, allow
   "Read and write permissions".
2. **Actions → Contribution snake → Run workflow** once. Until the first run finishes, the snake image
   shows its alt text.

GitHub disables scheduled workflows in public repositories after 60 days without repository activity;
re-enable it from the Actions tab (or push any commit) if the snake stops updating.

## Third-party cards

The Activity section uses public, rate-limited services. If one is down, GitHub shows the image's alt text
and the rest of the profile is unaffected.

| Card | Service |
| --- | --- |
| Stats, top languages | [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) public instance |
| Streak | [github-readme-streak-stats](https://github.com/DenverCoder1/github-readme-streak-stats) (`streak-stats.demolab.com`) |
| Tech badges | [shields.io](https://shields.io) |

A profile-view counter (komarev.com/ghpvc) was left out on purpose: it returned 404 through GitHub's
image proxy (camo) when this README was built, which would show as a broken image.

`include_all_commits` is intentionally off: the public stats instance often fails to fetch all-time commit
counts, while the default (last-year) count is reliable. If the public instance becomes unreliable, deploy
your own github-readme-stats instance on Vercel and swap the host in `README.md`.
