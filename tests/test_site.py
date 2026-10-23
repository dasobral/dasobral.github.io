"""Contract tests for the no-build, tabbed Daniel Sobral Blanco site."""

from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "projects.html", "research.html")
ALL_PAGES = PAGES + ("404.html",)
REDIRECTS = {
    "profile.html": "index.html#experience",
    "stack.html": "projects.html#stack",
}
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
        self.text = []
        self._open_tags = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))
        self._open_tags.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_endtag(self, tag):
        if tag in self._open_tags:
            del self._open_tags[len(self._open_tags) - 1 - self._open_tags[::-1].index(tag) :]

    def handle_data(self, data):
        hidden = {"head", "script", "style", "template"}
        if "body" in self._open_tags and not hidden.intersection(self._open_tags):
            self.text.append(data)

    def tags(self, name):
        return [attrs for tag, attrs in self.elements if tag == name]

    @property
    def ids(self):
        return [attrs["id"] for _, attrs in self.elements if "id" in attrs]

    @property
    def hrefs(self):
        return [attrs.get("href", "") for attrs in self.tags("a")]

    @property
    def visible_text(self):
        return " ".join(" ".join(self.text).split()).lower()


def parse_page(filename):
    parser = PageParser()
    parser.feed((ROOT / filename).read_text(encoding="utf-8"))
    parser.close()
    return parser


def meta_content(page, **match):
    for attrs in page.tags("meta"):
        if all(attrs.get(key, "").lower() == value.lower() for key, value in match.items()):
            return attrs.get("content", "")
    return None


def all_text():
    return " ".join(parse_page(filename).visible_text for filename in PAGES)


class SiteContractTests(unittest.TestCase):
    def test_pages_and_assets_exist(self):
        for filename in ALL_PAGES + tuple(REDIRECTS) + REQUIRED_ASSETS:
            with self.subTest(file=filename):
                self.assertTrue((ROOT / filename).is_file(), f"Missing {filename}")

    def test_pages_have_accessible_document_shell(self):
        for filename in ALL_PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                self.assertEqual(len(page.tags("main")), 1)
                self.assertEqual(page.tags("main")[0].get("id"), "main-content")
                self.assertTrue(any(href.endswith("#main-content") for href in page.hrefs), "Needs a skip link")
                for landmark in ("header", "nav", "footer"):
                    self.assertTrue(page.tags(landmark), f"Needs a <{landmark}> landmark")
                self.assertEqual(len(page.tags("h1")), 1, "Needs exactly one <h1>")
                self.assertEqual(page.tags("html")[0].get("lang"), "en")
                self.assertEqual(len(page.ids), len(set(page.ids)), "Element ids must be unique")

    def test_pages_have_unique_titles_and_descriptions(self):
        titles, descriptions = [], []
        for filename in PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                description = meta_content(page, name="description")
                self.assertTrue(description and 80 <= len(description) <= 320, "Needs a useful meta description")
                self.assertTrue(meta_content(page, property="og:title"), "Needs an Open Graph title")
                titles.append((ROOT / filename).read_text(encoding="utf-8").split("<title>")[1].split("</title>")[0])
                descriptions.append(description)
        self.assertEqual(len(set(titles)), len(PAGES), "Titles must be unique")
        self.assertEqual(len(set(descriptions)), len(PAGES), "Descriptions must be unique")

    def test_home_has_canonical_and_person_data(self):
        page = parse_page("index.html")
        canonical = [attrs.get("href") for attrs in page.tags("link") if attrs.get("rel") == "canonical"]
        self.assertEqual(canonical, ["https://dasobral.github.io/"])
        self.assertIn('"@type": "Person"', (ROOT / "index.html").read_text(encoding="utf-8"))

    def test_header_tabs_reach_every_page_and_mark_the_current_one(self):
        for filename in PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                for route in PAGES:
                    self.assertIn(route, page.hrefs, f"{filename} must link {route}")
                current = [attrs.get("href") for attrs in page.tags("a") if attrs.get("aria-current") == "page"]
                self.assertEqual(current, [filename], f"{filename} needs exactly one current tab")

    def test_in_page_tabs_point_at_panels(self):
        for filename in PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                tabs = [attrs.get("href", "") for attrs in page.tags("a") if "data-tab" in attrs]
                self.assertGreaterEqual(len(tabs), 2, f"{filename} needs in-page tabs")
                panels = {attrs["id"] for _, attrs in page.elements if "tab-panel" in attrs.get("class", "").split()}
                self.assertEqual({href[1:] for href in tabs}, panels, "Every tab needs one panel and vice versa")

    def test_internal_links_resolve(self):
        ids = {filename: set(parse_page(filename).ids) for filename in PAGES}
        for filename in PAGES:
            for href in parse_page(filename).hrefs:
                if href.startswith(("http", "mailto:")):
                    continue
                route, _, fragment = href.partition("#")
                route = route or filename
                with self.subTest(page=filename, href=href):
                    self.assertIn(route, PAGES, f"Unknown page {route}")
                    if fragment:
                        self.assertIn(fragment, ids[route], f"Broken fragment {href}")

    def test_external_links_open_in_a_new_tab_safely(self):
        for filename in ALL_PAGES:
            page = parse_page(filename)
            for attrs in page.tags("a"):
                if attrs.get("href", "").startswith("http"):
                    with self.subTest(page=filename, href=attrs["href"]):
                        self.assertEqual(attrs.get("target"), "_blank")
                        self.assertIn("noopener", attrs.get("rel", "").split())

    def test_references_are_numbered_once_and_in_order(self):
        page = parse_page("research.html")
        reference_ids = [i for i in page.ids if i.startswith("ref-")]
        self.assertEqual(reference_ids, [f"ref-{n}" for n in range(1, 12)])

    def test_site_states_positioning_and_stack(self):
        text = all_text()
        for phrase in ("daniel sobral blanco", "quside", "ph.d.", "entropy", "keys", "protocols", "authority", "qkd", "tls", "ipsec"):
            self.assertIn(phrase, text, f"Site must name {phrase!r}")

    def test_work_opens_on_the_stack_and_links_each_layer_to_evidence(self):
        page = parse_page("projects.html")
        tabs = [attrs.get("href") for attrs in page.tags("a") if "data-tab" in attrs]
        self.assertEqual(tabs[0], "#stack", "Work must open on the stack figure")
        for layer in ("authority", "protocols", "keys", "entropy"):
            self.assertIn(layer, page.visible_text)

    def test_about_includes_experience(self):
        page = parse_page("index.html")
        self.assertIn("experience", page.ids)
        self.assertIn("#experience", page.hrefs)

    def test_old_pages_redirect_to_their_new_place(self):
        for filename, target in REDIRECTS.items():
            with self.subTest(page=filename):
                page = parse_page(filename)
                self.assertEqual(meta_content(page, **{"http-equiv": "refresh"}), f"0; url={target}")
                self.assertIn(target, page.hrefs, "Needs a visible fallback link")
                self.assertEqual(meta_content(page, name="robots"), "noindex")

    def test_theme_switch_is_progressive(self):
        for filename in ALL_PAGES:
            with self.subTest(page=filename):
                page = parse_page(filename)
                buttons = [attrs for attrs in page.tags("button") if "theme-toggle" in attrs.get("class", "")]
                self.assertEqual(len(buttons), 1, "Needs one theme switch")
                self.assertIn("hidden", buttons[0], "The switch stays hidden until JavaScript can drive it")
                self.assertIn("localStorage.getItem('theme')", (ROOT / filename).read_text(encoding="utf-8"))

    def test_work_features_the_selected_projects(self):
        text = parse_page("projects.html").visible_text
        for project in ("agent trust", "openmls-qrand", "curso de criptografía post-cuántica", "qaoa portfolio", "pqc auth api"):
            self.assertIn(project, text, f"Work must feature {project!r}")
        for excluded in ("quside-curand", "entropy observatory", "codex inspector", "galaxyclassifier", "rust-hoex", "qkd-kem-bench"):
            self.assertNotIn(excluded, all_text(), f"Site must not feature {excluded!r}")

    def test_experience_covers_every_role_and_degree(self):
        text = parse_page("index.html").visible_text
        for milestone in (
            "application engineer",
            "indra",
            "universidad carlos iii de madrid",
            "university of geneva",
            "universidad complutense de madrid",
            "jean wurth prize",
        ):
            self.assertIn(milestone, text, f"Experience must include {milestone!r}")

    def test_research_links_every_verified_publication(self):
        hrefs = set(parse_page("research.html").hrefs)
        for publication in (
            "https://doi.org/10.1109/ISCC65549.2025.11325973",
            "https://doi.org/10.1109/ISCC65549.2025.11325762",
            "https://arxiv.org/abs/2507.09288",
            "https://doi.org/10.1088/1475-7516/2024/12/029",
            "https://doi.org/10.1088/1475-7516/2024/05/003",
            "https://arxiv.org/abs/2409.15170",
            "https://doi.org/10.1103/PhysRevD.107.083526",
            "https://doi.org/10.1093/mnrasl/slac124",
            "https://doi.org/10.1103/PhysRevD.104.063516",
            "https://doi.org/10.1088/1361-6382/ac3148",
            "https://doi.org/10.1103/PhysRevD.102.043506",
            "https://doi.org/10.13097/archive-ouverte/unige:178894",
        ):
            self.assertIn(publication, hrefs, f"Research must link {publication}")

    def test_every_page_offers_contact_and_profiles(self):
        for filename in PAGES:
            hrefs = parse_page(filename).hrefs
            for route in (
                "mailto:dasobral93@gmail.com",
                "https://github.com/dasobral",
                "https://orcid.org/0000-0001-9559-3651",
                "https://www.linkedin.com/in/dasobral",
            ):
                with self.subTest(page=filename, route=route):
                    self.assertIn(route, hrefs)

    def test_404_uses_root_anchored_assets_and_links(self):
        page = parse_page("404.html")
        for tag, attribute, expected in (
            ("link", "href", "/assets/css/styles.css"),
            ("link", "href", "/assets/icons/favicon.svg"),
            ("script", "src", "/assets/js/main.js"),
        ):
            with self.subTest(asset=expected):
                self.assertTrue(any(attrs.get(attribute) == expected for attrs in page.tags(tag)))
        local = [href for href in page.hrefs if not href.startswith(("mailto:", "http", "#"))]
        self.assertTrue(local)
        for href in local:
            with self.subTest(href=href):
                self.assertTrue(href.startswith("/"), "404 links must resolve from nested URLs")
                self.assertIn(href.lstrip("/").split("#")[0], PAGES)

    def test_pages_load_no_third_party_scripts_or_styles(self):
        for filename in ALL_PAGES:
            page = parse_page(filename)
            for attrs in page.tags("script") + page.tags("link"):
                source = attrs.get("src") or (attrs.get("href") if attrs.get("rel") in ("stylesheet", "icon") else "")
                with self.subTest(page=filename, source=source):
                    self.assertFalse(str(source).startswith(("http:", "https:", "//")))

    def test_pages_contain_no_placeholder_copy(self):
        for filename in ALL_PAGES:
            text = parse_page(filename).visible_text
            for filler in ("lorem ipsum", "tbd", "todo"):
                with self.subTest(page=filename, filler=filler):
                    self.assertNotIn(filler, text)


if __name__ == "__main__":
    unittest.main()
