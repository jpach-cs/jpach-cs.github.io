'''
Layer 2 check (h): no page returns a soft 404 -- an HTTP 200 whose body is
actually a "page not found" message. Jekyll can produce this if a layout
falls back unexpectedly; nginx serving the built static site would otherwise
give a real (hard) 404 for anything genuinely missing, which is a different,
correctly-detected failure mode covered by test_link_crawler.py.

Page set checked: everything the crawler finds reachable with a 200 (see
crawler.py), plus the syllabus/schedule pages, which are real, working pages
that the site's own nav happens not to link to correctly (see
test_syllabus_schedule.py's docstring) -- they still need to not be soft-404s.
'''

from __future__ import annotations

from urllib.parse import urlparse

from selenium.webdriver.remote.webdriver import WebDriver

from crawler import crawl, is_crawlable_page
from soft_404 import looks_like_soft_404

SEED_PATHS = ['/', '/teaching/']
EXTRA_PATHS = [
    f'/teaching/{course}/{page}'
    for course in ('csci-112', 'csci-232', 'csci-446', 'esof-322')
    for page in ('syllabus.html', 'schedule.html')
]


def _discover_ok_paths(base_url: str) -> set[str]:
    result = crawl(base_url, SEED_PATHS, max_pages=300)
    ok = {
        urlparse(url).path or '/'
        for url, status in result.checked.items()
        if status == 200 and is_crawlable_page(url)
    }
    ok.update(EXTRA_PATHS)
    return ok


def test_no_page_is_a_soft_404(visit, base_url: str) -> None:
    '''No reachable page should render as an HTTP-200-but-actually-not-found page.'''
    failures = []
    for path in sorted(_discover_ok_paths(base_url)):
        driver: WebDriver = visit(path)
        match = looks_like_soft_404(driver.page_source)
        if match:
            failures.append(f'{path}: looks like a soft 404 (matched "{match}")')
        if not driver.title.strip():
            failures.append(f'{path}: empty <title>')
    assert not failures, 'Soft-404-like page(s) found:\n' + '\n'.join(failures)
