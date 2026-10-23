# Daniel Sobral Blanco

Personal site of a quantum-safe security engineer and Ph.D. physicist: entropy, keys, protocols and agent authority, plus research in relativistic cosmology. One static page, no build step.

## Run locally

```sh
python3 -m http.server 8000
```

Then visit <http://localhost:8000>. There are no packages to install.

## Structure

The site has three pages, reached from tabs in the header: About, Work and Research. Longer content is split into in-page tabs, so Work and Research each fit one desktop screen.

- `index.html` — About: headline, Fig. 0, then Experience (§0) with Roles and Education & tools tabs
- `projects.html` — Work (§1): the four-layer stack (Fig. 1) as the first tab, then one tab per project
- `research.html` — Research (§2): publications in tabs by track; references are numbered [1]–[11]
- `profile.html`, `stack.html` — redirects to `index.html#experience` and `projects.html#stack`, kept so old links work
- `404.html` — error page with root-anchored assets for nested URLs
- `assets/css/styles.css` — the visual system: preprint typography, light and dark themes
- `assets/js/main.js` — progressive enhancement: theme switch, in-page tabs, footer year
- `assets/icons/favicon.svg` — favicon
- `tests/test_site.py` — standard-library content and structure contract

The header and footer are duplicated on every page, so update each copy when you change them. In-page tabs are plain links to panels. Without JavaScript they act as a table of contents and all panels show. With it, a link such as `projects.html#qkd-kem` or `research.html#ref-8` opens the tab that holds the target. External links open in a new tab (`target="_blank" rel="noopener noreferrer"`).

## Design

The page is set like a physics preprint: a serif text face (Palatino family, system fonts only), numbered sections, figures with captions, and a numbered reference list that the text cites. Code and metadata use a monospace face. One accent color, used like a reviewer's red pen. The theme follows the browser's `prefers-color-scheme` until the visitor uses the header switch. The choice is then saved in `localStorage` and applied by a one-line inline script in `<head>` before first paint, so pages don't flash. Without JavaScript the switch stays hidden and the browser setting wins.

## Verify

```sh
python3 -m unittest discover -s tests -v
node --check assets/js/main.js
git diff --check
```

Also check narrow (360 px) and 1440 × 900 viewports, both color schemes, arrow-key navigation between tabs, and JavaScript-disabled rendering in a browser.

## Content rules

- Every claim links to its evidence: a repository, a DOI or an arXiv record.
- Each project states its boundary, meaning what it does not prove.
- References are numbered [1]–[11]. Security papers come first. When you add one, renumber the list and every citation, and update the test.
- No impact metrics, employment details or scientific claims without a public source. No employer-internal projects.
- There are no analytics, cookies or third-party scripts.
