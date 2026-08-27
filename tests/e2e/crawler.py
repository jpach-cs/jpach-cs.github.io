'''
A small same-origin link/image crawler used by the Layer 2 link-integrity check
(item i: "every <a href> and <img src> resolves").

Design note: this deliberately uses `requests`, not the Selenium WebDriver, to
walk pages and check status codes. The WebDriver protocol has no built-in way
to read the HTTP status code of a navigation (that requires wiring up Chrome
DevTools Protocol network logging, which is fragile across Chrome/driver
versions and unnecessary here since the site is static, server-rendered HTML
with no client-side routing). Selenium is used elsewhere in this suite
(conftest.py, test_home_and_nav.py, test_course_pages.py, ...) for what it is
actually good at: rendering pages in a real browser and driving interactions
like clicking. Using the right tool for each half of the job is simpler and
far faster than forcing everything through the browser -- crawling ~40 pages
and ~300 links via `requests` takes well under a second; doing the same by
loading every single link in a real browser would take minutes.
'''

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

SKIP_SCHEMES = ('mailto:', 'javascript:', 'tel:')
NON_PAGE_EXTENSIONS = (
    '.pdf', '.svg', '.png', '.jpg', '.jpeg', '.gif', '.ico',
    '.css', '.js', '.woff', '.woff2', '.ttf',
)


class _LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.imgs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_dict = dict(attrs)
        if tag == 'a':
            href = attr_dict.get('href')
            if href:
                self.hrefs.append(href)
        elif tag == 'img':
            src = attr_dict.get('src')
            if src:
                self.imgs.append(src)


def extract_links(html: str) -> tuple[list[str], list[str]]:
    '''Parse `html` and return (hrefs, img srcs) found in it, in document order.'''
    parser = _LinkExtractor()
    parser.feed(html)
    return parser.hrefs, parser.imgs


def is_same_origin(url: str, base_url: str) -> bool:
    '''Return True if `url` has no netloc (relative) or matches `base_url`'s netloc.'''
    return urlparse(url).netloc in ('', urlparse(base_url).netloc)


def is_crawlable_page(url: str) -> bool:
    '''Return True if `url` looks like an HTML page worth crawling further, not an asset.'''
    path = urlparse(url).path.lower()
    return not path.endswith(NON_PAGE_EXTENSIONS)


@dataclass
class CrawlResult:
    '''The outcome of a `crawl()` call: every URL checked, and who linked to it.'''

    # url -> status code, or -1 for a connection-level failure
    checked: dict[str, int] = field(default_factory=dict)
    # url -> list of pages that referenced it
    referenced_by: dict[str, list[str]] = field(default_factory=dict)

    def broken(self) -> dict[str, list[str]]:
        '''Return the subset of `referenced_by` whose URL did not check out as 200.'''
        return {url: refs for url, refs in self.referenced_by.items() if self.checked[url] != 200}


def crawl(base_url: str, seed_paths: list[str], max_pages: int = 100) -> CrawlResult:
    '''
    Breadth-first crawl starting from `seed_paths`, following every same-origin
    `<a href>` and `<img src>` found on each visited HTML page. Non-HTML
    resources (PDFs, images, CSS, ...) are checked but not crawled further.
    '''
    session = requests.Session()
    result = CrawlResult()
    visited_pages: set[str] = set()
    queue: list[str] = [urljoin(base_url + '/', p) for p in seed_paths]

    def check(url: str, referrer: str) -> int:
        result.referenced_by.setdefault(url, [])
        if referrer not in result.referenced_by[url]:
            result.referenced_by[url].append(referrer)
        if url in result.checked:
            return result.checked[url]
        try:
            response = session.get(url, timeout=15, allow_redirects=True)
            status = response.status_code
        except requests.RequestException:
            status = -1
        result.checked[url] = status
        return status

    while queue and len(visited_pages) < max_pages:
        url = queue.pop(0).split('#', 1)[0]
        if url in visited_pages or not is_same_origin(url, base_url):
            continue
        visited_pages.add(url)
        status = check(url, referrer='<seed>')
        if status != 200 or not is_crawlable_page(url):
            continue

        try:
            page = session.get(url, timeout=15)
        except requests.RequestException:
            continue

        hrefs, imgs = extract_links(page.text)
        for raw_link in hrefs + imgs:
            if raw_link.startswith(SKIP_SCHEMES):
                continue
            absolute = urljoin(url, raw_link).split('#', 1)[0]
            if not is_same_origin(absolute, base_url):
                continue
            check(absolute, referrer=url)
            if is_crawlable_page(absolute) and absolute not in visited_pages:
                queue.append(absolute)

    return result
