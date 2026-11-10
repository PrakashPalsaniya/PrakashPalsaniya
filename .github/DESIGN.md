# Profile artwork

The README is built from local SVGs. It needs no external image service, custom
JavaScript, font download, or rendering service on GitHub. Native links and
expandable details remain usable alongside the artwork.

- `generate_profile.py` owns the copy, project links, README markup, and static artwork.
- `profile_svg.py` owns the shared colors, drawing primitives, and SVG animation.
- `generate_activity.py` collects public GitHub data; `activity_layout.py` draws it.
- `activity-data.json` is the last successful, dated public snapshot.

From the profile repository root:

```sh
python .github/generate_profile.py
python .github/generate_activity.py --cached
```

Omit `--cached` to refresh data from GitHub. The existing daily GitHub Action
updates the four activity SVGs and snapshot together. A failed fetch or incomplete
calendar fails the job and leaves the previous dated cards in place.

Each artwork has dark, light, and mobile variants. `<picture>` selects mobile
compositions at viewport widths up to 600px. Images have accessible descriptions;
the SVG animations stop when `prefers-reduced-motion: reduce` is enabled.
Static frames also work when an image renderer disables animation. The FinMate
chat is an illustrative interaction, not an actual user record or usage metric.

For a local visual preview, install the optional Python `markdown` package and run:

```sh
python .github/preview_profile.py
```

Open `.preview/index.html` in a browser. Its Light/Dark controls apply only to the
preview; GitHub selects its theme through the native picture sources. `.preview/`
is ignored. This preview approximates GitHub's README layout, rather than its full
profile page or sanitization pipeline.
