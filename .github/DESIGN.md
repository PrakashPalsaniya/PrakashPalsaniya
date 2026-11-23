# GitHub profile

The header and contribution panel use compact, generated SVG cards. The header
has a navy/purple gradient; contribution cards use cyan, violet, and amber.
Light and dark themes each have a desktop and mobile layout, selected with
GitHub-supported `picture` elements. These are vector UI cards, with no screenshots.

GitHub strips custom CSS from README HTML, so card typography and gradients live
inside the SVGs. Sora headings and numbers, Public Sans supporting text, and IBM
Plex Mono labels are converted to vector paths using bundled fonts. The SVGs
contain no scripts, external images, or font requests. Titles, descriptions,
and README alt text preserve the card content for accessibility.

Contact links, the two-by-two project grid, the expandable architecture section,
the toolbox, and language details remain native HTML. The preview uses local
assets and approximates GitHub's surrounding styles.

- `generate_profile.py` owns the copy, project links, README, and activity summary.
- `profile_cards.py` renders the eight themed card variants.
- `svg_typography.py` outlines the bundled fonts in `fonts/`, alongside their OFL licenses.
- `generate_activity.py` collects public GitHub data and regenerates the cards and README.
- `activity-data.json` is the last successful, dated public snapshot.

From the profile repository root:

```sh
python -m pip install -r .github/requirements.txt
python .github/generate_profile.py
python .github/generate_activity.py --cached
```

Omit `--cached` to refresh data from GitHub. The daily GitHub Action updates the
README, cards, and snapshot together. A failed fetch or incomplete calendar fails
the job and leaves the published profile unchanged. Every card variant is rendered
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
