# Daniel Sobral Blanco Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a complete, responsive, accessible multi-page professional portfolio directly from GitHub Pages.

**Architecture:** Four semantic static HTML pages share a focused CSS design system and a small progressive-enhancement JavaScript file. A standard-library Python test suite validates structure, content, links, metadata, and deployment assumptions without introducing a build dependency.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python 3 `unittest`

**Spec:** `docs/superpowers/specs/2026-09-17-portfolio-site-design.md`

## Global Constraints

- Use plain HTML, CSS, and JavaScript with no package manager, framework, analytics, cookies, or external font dependency.
- Create `index.html`, `profile.html`, `projects.html`, and `research.html` with consistent navigation and footer.
- Feature only current work named in the spec; do not feature the four repositories explicitly excluded there.
- Every public claim must remain within the boundaries documented by its public source.
- The site must remain fully navigable and readable with JavaScript disabled.
- Meet the accessibility, responsive-layout, reduced-motion, and metadata requirements in the spec.

---

### Task 1: Define the site contract with failing tests

**Files:**
- Create: `tests/test_site.py`

**Interfaces:**
- Consumes: design requirements from the spec
- Produces: `python3 -m unittest discover -s tests -v` as the repository-wide verification command

- [ ] **Step 1: Write tests for required pages and shared assets**

Create standard-library tests that require the four HTML pages, `assets/css/styles.css`, `assets/js/main.js`, and `404.html`.

- [ ] **Step 2: Write tests for semantic structure and metadata**

For every page, assert one `main`, a skip link, header/navigation/footer landmarks, a unique non-empty `title`, a useful meta description, viewport metadata, shared stylesheet/script references, and an `aria-current="page"` navigation link.

- [ ] **Step 3: Write tests for content and link safety**

Assert the current featured project names, both research tracks, core profile positioning, GitHub/LinkedIn/ORCID/email routes, no excluded-project names on the Projects page, no placeholder text, and `rel="noreferrer"` on external new-tab links.

- [ ] **Step 4: Run tests and verify the expected failure**

Run: `python3 -m unittest discover -s tests -v`

Expected: failures because the required site files do not exist.

### Task 2: Implement the static portfolio

**Files:**
- Create: `index.html`
- Create: `profile.html`
- Create: `projects.html`
- Create: `research.html`
- Create: `404.html`
- Create: `assets/css/styles.css`
- Create: `assets/js/main.js`
- Create: `assets/icons/favicon.svg`
- Modify: `README.md`

**Interfaces:**
- Consumes: the HTML and content contract in `tests/test_site.py`
- Produces: a directly deployable GitHub Pages site and shared `.site-header`, `.site-nav`, `.site-footer`, project-card, publication-list, and reveal patterns

- [ ] **Step 1: Implement shared document shell and navigation**

Add metadata, skip links, desktop/mobile navigation, active-page state, shared footer, social/contact links, and favicon to every page.

- [ ] **Step 2: Implement Home and Profile**

Write the profile-led landing page and full professional narrative/timeline using verified public facts and careful claim boundaries.

- [ ] **Step 3: Implement Projects and Research**

Describe the six current projects and two research tracks with repository, DOI/arXiv, ORCID, and thesis/profile links.

- [ ] **Step 4: Implement the visual system and progressive enhancement**

Add responsive editorial layouts, CSS-native technical motifs, focus/hover states, mobile navigation, reveal transitions, reduced-motion handling, and graceful no-JavaScript behavior.

- [ ] **Step 5: Add deployment fallback and documentation**

Create a branded 404 page and update README with structure, local preview, validation, and GitHub Pages deployment notes.

- [ ] **Step 6: Run tests until green**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass.

### Task 3: Cross-browser and accessibility verification

**Files:**
- Modify if needed: HTML, CSS, JavaScript, tests, and README files from Task 2

**Interfaces:**
- Consumes: completed static site
- Produces: verified final repository state

- [ ] **Step 1: Validate HTML references and local serving**

Run the unit suite and start `python3 -m http.server` long enough to request every page and shared asset with `curl`, asserting HTTP 200 responses.

- [ ] **Step 2: Run syntax and repository hygiene checks**

Run `node --check assets/js/main.js`, inspect `git diff --check`, and search for `TODO`, `TBD`, placeholder copy, accidental secrets, and excluded project names in user-facing project content.

- [ ] **Step 3: Inspect representative desktop and mobile renders**

Capture or inspect Home, Projects, and Research at desktop and mobile widths. Correct overflow, hierarchy, focus, navigation, and spacing defects.

- [ ] **Step 4: Run the complete verification suite again**

Run all commands fresh and record exact passing results before completion.

