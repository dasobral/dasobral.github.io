# Daniel Sobral Blanco Portfolio — Design Specification

## Purpose

Build a polished multi-page GitHub Pages portfolio that presents Daniel Sobral Blanco as a software engineer and physicist working across quantum-safe security, trustworthy agent systems, scientific computing, and research. The site is profile-led: projects and publications support the professional narrative rather than replace it.

## Audience

- Technical peers and collaborators
- Engineering and research teams
- Conference, teaching, and consulting contacts
- Visitors arriving from GitHub, LinkedIn, ORCID, or a publication

## Editorial direction

The central message is: **rigorous research translated into trustworthy systems**.

Copy must be direct, specific, and modest about claim boundaries. Current public work receives priority. Older repositories named during discovery (`qkd-kem-bench`, `qkd-etsi-api-c-wrapper`, `GalaxyClassifier`, and `rust-hoex`) are not featured.

## Information architecture

### Home (`index.html`)

- Concise introduction and professional positioning
- Three-domain overview: quantum-safe systems, trustworthy agents, scientific computing
- Selected current work preview
- Research transition and clear routes to Profile, Projects, Research, GitHub, LinkedIn, and email

### Profile (`profile.html`)

- Narrative biography connecting physics, software engineering, and security
- Current focus and working principles
- Career and education timeline
- Capabilities without an inflated skill-cloud treatment

### Projects (`projects.html`)

- Featured current projects with problem, approach, status/claim boundary, technology, and repository links
- Primary work: Agent Trust, OpenMLS QRNG, Portable Skills, Codex Inspector, QAOA Portfolio Optimizer, and the post-quantum cryptography course
- No GitHub popularity metrics or fabricated impact claims

### Research (`research.html`)

- Two research tracks: quantum-safe communications and relativistic cosmology
- Selected publication list using verified public metadata and direct DOI/arXiv links
- PhD thesis/research context and ORCID link

## Visual system

- Editorial, technical, and restrained rather than a generic developer dashboard
- Deep ink background, warm off-white typography, cyan signal color, and muted amber secondary accent
- Large serif display type paired with a crisp system sans-serif body
- Thin rules, generous whitespace, asymmetric layouts, subtle grid/orbit motifs built with CSS/SVG
- Motion is understated and disabled under `prefers-reduced-motion`
- Responsive from small phones through wide desktop screens

## Technical architecture

- Plain semantic HTML, one shared CSS file, and one small progressive-enhancement JavaScript file
- No framework, bundler, runtime dependency, analytics, cookies, or external font dependency
- Relative links work both at the GitHub Pages root and from local files
- Shared navigation and footer are duplicated deliberately across four small static pages for zero-build deployment
- JavaScript controls the mobile menu, active-page indication fallback, scroll reveal, and current footer year; core content remains usable without it

## Accessibility and quality

- Skip link, landmarks, logical heading hierarchy, visible focus states, and descriptive link labels
- Mobile navigation exposes `aria-expanded` and closes on navigation/Escape
- Decorative visuals are hidden from assistive technology
- Color contrast targets WCAG AA
- Tests validate page existence, shared navigation, unique titles/descriptions, semantic landmarks, key content, safe external-link attributes, and absence of placeholder text

## Source boundaries

Public claims are based on Daniel's GitHub profile and current repositories, ORCID record, University of Geneva profile, and linked publications. The site avoids sensitive details and excludes third-party logos or imagery. Contact uses the email already published on Daniel's GitHub profile.

