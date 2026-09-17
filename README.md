# Daniel Sobral Blanco

A small, no-build portfolio for a software engineer and physicist working across quantum-safe security, trustworthy agent systems, and scientific computing.

## Run locally

Open `index.html` directly, or serve the repository with Python:

```sh
python3 -m http.server 8000
```

Then visit <http://localhost:8000>. There are no packages to install or build steps.

## Structure

- `index.html` — introduction, areas of focus, and selected work
- `profile.html` — background, working principles, and education
- `projects.html` — six selected public projects and their scope
- `research.html` — research tracks, publications, and doctoral context
- `404.html` — custom error page
- `assets/css/styles.css` — shared responsive visual system
- `assets/js/main.js` — progressive enhancement for navigation, year, and reveals
- `assets/icons/favicon.svg` — constellation favicon
- `tests/test_site.py` — standard-library content and structure contract

Navigation and footers are intentionally duplicated across the static pages. Update each copy when changing shared routes or contact details. Core content and navigation work without JavaScript. Motion respects `prefers-reduced-motion`.

## Verify

```sh
python3 -m unittest discover -s tests -v
node --check assets/js/main.js
git diff --check
```

Also check narrow and wide viewports, keyboard navigation, the mobile menu, reduced motion, and JavaScript-disabled rendering in a browser. The contract tests do not replace visual or interaction checks.

## Publish

The site is ready to be served as static files by GitHub Pages. In the repository’s Pages settings, choose the branch containing the site and the repository root as the publishing directory. No custom domain or deployment workflow is required.

The HTML uses relative local links, system fonts, and local assets. There are no analytics, cookies, third-party scripts, or runtime dependencies. Publication and repository links lead to their public source records; external destinations open in the same tab.

## Content

Keep project descriptions tied to the linked repositories and distinguish research prototypes from production software. Academic context is linked to the University of Geneva and ORCID. Do not add impact metrics, employment dates, or scientific claims without a public source.
