'''
Layer 2 check (i): every `<a href>` and `<img src>` on the crawled pages
resolves (no 404s).

Crawls from "/" and "/teaching/" across the live site (must already be
running; see tests/README.md and crawler.py for why this uses `requests`
rather than driving every single link through the browser).

As of writing, the site has ~250 broken same-origin links -- almost entirely
the same missing lecture/lab content Layer 1 finds in the source tree, plus a
few HTML-layer-only defects Layer 1 cannot see:
  * the home page links to "/research/", which 404s (no research page exists);
  * each course's "syllabus"/"schedule" nav links point at extensionless URLs
    but Jekyll renders those pages at "syllabus.html"/"schedule.html", so
    every one of those 8 links 404s;
  * "/teaching/csci-232/assignments/ass01/" returns 403 (not 404) because that
    directory has no index.html, only index.pdf, so nginx has nothing to serve
    and directory listing is off.

This test asserts there are zero broken same-origin links/images and fails
today because that content is genuinely incomplete. That is by design: the
suite is meant to stay red, with a readable list of exactly what is broken and
where it was linked from, until the underlying content is fixed.
'''

from __future__ import annotations

from collections import defaultdict
from urllib.parse import urlparse

from crawler import crawl
from link_report import format_broken_links_report

SEED_PATHS = ['/', '/teaching/']


def _to_path(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path or '/'


def _format_broken(broken: dict[str, list[str]]) -> str:
    '''Group broken links (by url -> referrers) by referring page and format a report.'''
    by_source: dict[str, list[str]] = defaultdict(list)
    for url, referrers in broken.items():
        for referrer in referrers:
            by_source[referrer].append(_to_path(url))
    header = f'{len(broken)} broken same-origin link(s)/image(s) found:'
    return format_broken_links_report(header, dict(by_source))


def test_crawl_finds_pages(base_url: str) -> None:
    '''Sanity check: the crawl itself must actually reach a meaningful chunk of the site.'''
    result = crawl(base_url, SEED_PATHS, max_pages=300)
    assert len(result.checked) > 10, (
        f'Crawl from {SEED_PATHS} only found {len(result.checked)} URLs; '
        'expected dozens. Is the site actually serving content at this base_url?'
    )


def test_no_broken_links(base_url: str) -> None:
    '''Every same-origin <a href>/<img src> found while crawling must resolve.'''
    result = crawl(base_url, SEED_PATHS, max_pages=300)
    broken = result.broken()
    assert not broken, _format_broken(broken)
