"""Contract tests for the no-build Daniel Sobral Blanco portfolio."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_PAGES = ("index.html", "profile.html", "projects.html", "research.html")
ALL_PAGES = PRIMARY_PAGES + ("404.html",)
REQUIRED_ASSETS = (
    "assets/css/styles.css",
    "assets/js/main.js",
    "assets/icons/favicon.svg",
)


class PageParser(HTMLParser):
    """Small DOM-like record of the meaningful parts of a static HTML page."""

    def __init__(self):
        super().__init__()
        self.elements = []
        self.links = []
        self.text = []
        self._open_tags = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if tag == "a":
            self.links.append((attributes, tuple(self._open_tags)))
        self._open_tags.append(tag)

    def handle_startendtag(self, tag, attrs):
        attributes = dict(attrs)
        self.elements.append((tag, attributes))
        if tag == "a":
            self.links.append((attributes, tuple(self._open_tags)))

    def handle_endtag(self, tag):
        if tag in self._open_tags:
            del self._open_tags[len(self._open_tags) - 1 - self._open_tags[::-1].index(tag) :]

    def handle_data(self, data):
        non_visible_containers = {"head", "script", "style", "template"}
        if "body" in self._open_tags and not non_visible_containers.intersection(self._open_tags):
            self.text.append(data)

    def tags(self, name):
        return [attrs for tag, attrs in self.elements if tag == name]

    @property
    def visible_text(self):
        return " ".join(self.text).lower()


def parse_page(filename):
    page = ROOT / filename
    parser = PageParser()
    if not page.is_file():
        return parser
    parser.feed(page.read_text(encoding="utf-8"))
    parser.close()
    return parser


def normalized_route(href):
    """Return a local page route without a same-page fragment or query string."""
    route = href.split("#", 1)[0].split("?", 1)[0].strip()
    while route.startswith("./"):
        route = route[2:]
    return route.lstrip("/")


class PortfolioContractTests(unittest.TestCase):
    def test_required_pages_exist(self):
        for filename in ALL_PAGES:
            self.assertTrue((ROOT / filename).is_file(), f"Missing required page: {filename}")

    def test_shared_assets_exist(self):
        for filename in REQUIRED_ASSETS:
            self.assertTrue((ROOT / filename).is_file(), f"Missing shared asset: {filename}")

    def test_404_assets_and_recovery_links_work_from_nested_missing_urls(self):
        page = parse_page("404.html")
        for tag, attribute, expected in (
            ("link", "href", "/assets/css/styles.css"),
            ("link", "href", "/assets/icons/favicon.svg"),
            ("script", "src", "/assets/js/main.js"),
        ):
            with self.subTest(asset=expected):
                self.assertTrue(
                    any(attrs.get(attribute) == expected for attrs in page.tags(tag)),
                    f"404.html must anchor {expected} at the site root for nested missing URLs",
                )

        recovery_links = [
            attrs.get("href", "")
            for attrs in page.tags("a")
            if normalized_route(attrs.get("href", "")) in PRIMARY_PAGES
        ]
        self.assertTrue(recovery_links, "404.html needs primary recovery links")
        for href in recovery_links:
            with self.subTest(recovery=href):
                self.assertIn(
                    href,
                    ("/index.html", "/profile.html", "/projects.html", "/research.html"),
                    "Every 404 recovery link must reach the site root from nested missing URLs",
                )
        self.assertTrue(
            {"/index.html", "/profile.html", "/projects.html", "/research.html"}
            <= set(recovery_links),
            "404.html must expose root-anchored routes to all primary pages",
        )

    def test_primary_pages_have_accessible_document_shell(self):
        for filename in PRIMARY_PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                self.assertEqual(len(page.tags("main")), 1, f"{filename} must contain exactly one <main>")
                self.assertTrue(page.tags("header"), f"{filename} needs a <header> landmark")
                self.assertTrue(page.tags("nav"), f"{filename} needs a <nav> landmark")
                self.assertTrue(page.tags("footer"), f"{filename} needs a <footer> landmark")
                self.assertTrue(
                    any(attrs.get("href") == "#main-content" for attrs in page.tags("a")),
                    f"{filename} needs a skip link targeting #main-content",
                )
                self.assertEqual(
                    page.tags("main")[0].get("id"),
                    "main-content",
                    f"{filename} must give its <main> id=main-content for the skip link",
                )

    def test_primary_pages_have_complete_shared_metadata(self):
        titles = []
        for filename in PRIMARY_PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                titles_for_page = page.tags("title")
                self.assertEqual(len(titles_for_page), 1, f"{filename} needs exactly one <title>")
                title = self._title_value(filename)
                self.assertGreaterEqual(len(title), 8, f"{filename} needs a useful non-empty <title>")
                descriptions = [
                    attrs.get("content", "")
                    for attrs in page.tags("meta")
                    if attrs.get("name", "").lower() == "description"
                ]
                self.assertEqual(len(descriptions), 1, f"{filename} needs one meta description")
                self.assertGreaterEqual(
                    len(descriptions[0].strip()), 80, f"{filename} meta description must be at least 80 characters"
                )
                self.assertTrue(
                    any(attrs.get("name", "").lower() == "viewport" for attrs in page.tags("meta")),
                    f"{filename} needs viewport metadata",
                )
                self.assertTrue(
                    any(
                        "icon" in attrs.get("rel", "").lower().split()
                        and "assets/icons/favicon.svg" in attrs.get("href", "")
                        for attrs in page.tags("link")
                    ),
                    f"{filename} must reference the shared SVG favicon",
                )
                self.assertTrue(
                    any(
                        "stylesheet" in attrs.get("rel", "").lower().split()
                        and "assets/css/styles.css" in attrs.get("href", "")
                        for attrs in page.tags("link")
                    ),
                    f"{filename} must load assets/css/styles.css",
                )
                self.assertTrue(
                    any(
                        "assets/js/main.js" in attrs.get("src", "") and "defer" in attrs
                        for attrs in page.tags("script")
                    ),
                    f"{filename} must load assets/js/main.js with defer",
                )
                titles.append(title)
        self.assertEqual(len(set(titles)), len(PRIMARY_PAGES), "Primary pages need unique titles")

    def _title_value(self, filename):
        class TitleParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.in_title = False
                self.values = []

            def handle_starttag(self, tag, attrs):
                self.in_title = tag == "title"

            def handle_endtag(self, tag):
                if tag == "title":
                    self.in_title = False

            def handle_data(self, data):
                if self.in_title:
                    self.values.append(data)

        parser = TitleParser()
        page = ROOT / filename
        if not page.is_file():
            return ""
        parser.feed(page.read_text(encoding="utf-8"))
        return " ".join(parser.values).strip()

    def test_primary_navigation_reaches_every_primary_route(self):
        expected_routes = {"index.html", "profile.html", "projects.html", "research.html"}
        for filename in PRIMARY_PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                nav_links = [attrs for attrs, ancestors in page.links if "nav" in ancestors]
                hrefs = {normalized_route(attrs.get("href", "")) for attrs in nav_links}
                self.assertTrue(
                    expected_routes <= hrefs,
                    f"{filename} navigation must reach Home, Profile, Projects, and Research",
                )
                active = [attrs for attrs in nav_links if attrs.get("aria-current") == "page"]
                self.assertEqual(len(active), 1, f"{filename} needs exactly one aria-current=page nav link")
                if len(active) == 1:
                    self.assertEqual(
                        normalized_route(active[0].get("href", "")),
                        filename,
                        f"{filename} aria-current=page must identify its own route",
                    )

    def test_external_new_tab_links_use_noreferrer(self):
        for filename in ALL_PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                for attrs in page.tags("a"):
                    href = attrs.get("href", "")
                    if attrs.get("target") == "_blank" and href.lower().startswith(("https://", "http://")):
                        rel_tokens = attrs.get("rel", "").lower().split()
                        self.assertIn(
                            "noreferrer",
                            rel_tokens,
                            f"{filename} external new-tab link {attrs.get('href', '')!r} must include rel=noreferrer",
                        )

    def test_site_exposes_professional_and_contact_routes(self):
        links = [attrs.get("href", "") for filename in ALL_PAGES for attrs in parse_page(filename).tags("a")]
        for label, route in {
            "GitHub": "github.com",
            "LinkedIn": "linkedin.com",
            "ORCID": "orcid.org",
            "email": "mailto:",
        }.items():
            self.assertTrue(any(route in href.lower() for href in links), f"Site needs a {label} route")

    def test_home_states_the_professional_positioning_and_domains(self):
        text = parse_page("index.html").visible_text
        for phrase in (
            "software engineer",
            "physicist",
            "quantum technologies",
            "secure software",
            "scientific computing",
        ):
            self.assertIn(phrase, text, f"Home page must name {phrase!r}")

    def test_home_dsb_logo_explains_the_professional_arc(self):
        page = parse_page("index.html")
        text = page.visible_text
        for phrase in ("cosmology", "cryptography", "software"):
            self.assertIn(phrase, text, f"Home orbital figure must name {phrase!r}")
        self.assertTrue(
            any(attrs.get("data-dsb-logo") == "true" for attrs in page.tags("svg")),
            "Home needs an explicit accessible dsb logo graphic",
        )

    def test_profile_contains_the_complete_professional_timeline(self):
        text = parse_page("profile.html").visible_text
        for milestone in (
            "Quside",
            "Indra",
            "Pervasive Computing Laboratory",
            "University of Geneva",
            "2025",
            "2024",
            "2020–2024",
        ):
            self.assertIn(milestone.lower(), text, f"Profile must include career milestone {milestone!r}")

    def test_projects_features_only_the_current_named_work(self):
        text = parse_page("projects.html").visible_text
        for project in (
            "entropy observatory",
            "agent trust",
            "openmls qrng",
            "portable skills",
            "codex inspector",
            "qaoa portfolio optimizer",
            "post-quantum cryptography course",
        ):
            self.assertIn(project, text, f"Projects page must feature {project!r}")
        self.assertNotIn("quside-curand", text, "Projects page must not feature employer-specific Quside-cuRAND work")
        for excluded in ("qkd-kem-bench", "qkd-etsi-api-c-wrapper", "galaxyclassifier", "rust-hoex"):
            self.assertNotIn(excluded, text, f"Projects page must not feature obsolete work {excluded!r}")

    def test_research_includes_tracks_and_verified_publication_links(self):
        page = parse_page("research.html")
        for track in ("quantum-safe communications", "relativistic cosmology"):
            self.assertIn(track, page.visible_text, f"Research page must name {track!r}")
        hrefs = {attrs.get("href", "") for attrs in page.tags("a")}
        for publication in (
            "https://arxiv.org/abs/2507.09288",
            "https://arxiv.org/abs/2503.07196",
            "https://arxiv.org/abs/2502.06657",
            "https://doi.org/10.1088/1475-7516/2024/12/029",
            "https://doi.org/10.1088/1475-7516/2024/05/003",
            "https://arxiv.org/abs/2409.15170",
            "https://doi.org/10.1103/PhysRevD.107.083526",
            "https://doi.org/10.1093/mnrasl/slac124",
            "https://doi.org/10.1103/PhysRevD.102.043506",
        ):
            self.assertIn(publication, hrefs, f"Research page must link verified publication {publication}")

    def test_user_facing_pages_contain_no_placeholder_copy(self):
        for filename in ALL_PAGES:
            with self.subTest(page=filename):
                text = parse_page(filename).visible_text
                for filler in ("lorem ipsum", "tbd", "todo"):
                    self.assertNotIn(filler, text, f"{filename} contains placeholder copy {filler!r}")


if __name__ == "__main__":
    unittest.main()
