# GitHub profile

The README uses a small PNG title badge displayed at 320 × 64 pixels and three
contribution badges displayed at 128 × 36 pixels. Badges wrap naturally on narrow
screens. There are no large panels, separate mobile card layouts, or SVG references
in the published README. Introduction text, links, project grids, architecture,
toolbox, and language details use native GitHub HTML.

Badges preserve the navy/purple header gradient and cyan, violet, and amber
contribution colors. Pillow renders bundled Public Sans at twice the display
resolution: weight 600 for the title and numbers, 500 for metric labels, and
400 for supporting text. Badge words have 1.2px of extra spacing (1.8px in the title).
Native section headings use `h3`, project and tool subheadings are bold, and
breakable third-em spaces give headings and project text a slightly wider word
gap. Light and dark variants are
selected with `picture` elements. Explicit display widths keep images compact,
and the title keeps its aspect ratio as it shrinks on narrow screens. Alt text preserves each badge's
content. These are generated graphics, with no screenshots or external services.

The preview uses local assets and approximates GitHub's surrounding styles.

- `generate_profile.py` owns the copy, project links, README, and activity summary.
- `profile_cards.py` renders the eight small PNG badge variants using bundled fonts and OFL licenses in `fonts/`.
- `generate_activity.py` collects public GitHub data and regenerates the badges and README.
- `activity-data.json` is the last successful, dated public snapshot.

From the profile repository root:

```sh
python -m pip install -r .github/requirements.txt
python .github/generate_profile.py
python .github/generate_activity.py --cached
```

Omit `--cached` to refresh data from GitHub. The daily GitHub Action updates the
README, badges, and snapshot together. A failed fetch or incomplete calendar fails
the job and leaves the published profile unchanged. Every badge variant is rendered
before any assets are written. The contribution totals use the
snapshot's refresh date for their rolling 365-day and 90-day windows. Languages
count primary languages across public nonfork repositories.

For a local visual preview, install the optional Python `markdown` package and run:

```sh
python .github/preview_profile.py
```

Open `.preview/index.html` in a browser. The Light/Dark controls apply only to the
preview. `.preview/` is ignored. The preview approximates GitHub's README layout,
rather than its full profile page or sanitization pipeline.
