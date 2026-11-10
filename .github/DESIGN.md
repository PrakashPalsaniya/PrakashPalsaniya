# GitHub profile

The profile uses GitHub-supported HTML: normal divs for the introduction and
contact, a compact activity table, a two-by-two project grid, one expandable
architecture section, and a two-by-two toolbox. Text, links, and flow descriptions
replace the SVG artwork. The README contains no image banners or SVG references.

GitHub strips custom CSS from READMEs. Layout uses supported table, width,
alignment, and vertical-alignment attributes; GitHub supplies typography, colors,
borders, themes, and narrow-screen handling. The local HTML/CSS preview emulates
those native styles; custom CSS is not embedded in the published README.

- `generate_profile.py` owns the copy, project links, README, and activity summary.
- `generate_activity.py` collects public GitHub data and regenerates the README.
- `activity-data.json` is the last successful, dated public snapshot.

From the profile repository root:

```sh
python .github/generate_profile.py
python .github/generate_activity.py --cached
```

Omit `--cached` to refresh data from GitHub. The daily GitHub Action updates the
README and snapshot together. A failed fetch or incomplete calendar fails the
job and leaves the published profile unchanged. The contribution totals use the
snapshot's refresh date for their rolling 365-day and 90-day windows. Languages
count primary languages across public nonfork repositories.

For a local visual preview, install the optional Python `markdown` package and run:

```sh
python .github/preview_profile.py
```

Open `.preview/index.html` in a browser. The Light/Dark controls apply only to the
preview. `.preview/` is ignored. The preview approximates GitHub's README layout,
rather than its full profile page or sanitization pipeline.
