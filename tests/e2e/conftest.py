'''
Shared fixtures for the Layer 2 (end-to-end, Selenium) test suite.

Two things must already be running before this suite starts, neither of which
it starts itself (see tests/README.md for exact commands):

  1. The site, at BASE_URL (default http://localhost:8082).
  2. A selenium/standalone-chrome container, reachable at SELENIUM_REMOTE_URL
     (default http://localhost:4444/wd/hub).

Both are overridable via environment variables so this works unchanged in CI,
where the selenium container's published port or the site's port may differ.

Two different base URLs, deliberately:
    `base_url`         -- used by plain HTTP checks (`requests`) that run on
                           the same host as pytest itself.
    `browser_base_url` -- used by Selenium navigations, which happen *inside*
                           the selenium/standalone-chrome container. That
                           container cannot reach the site via "localhost"
                           (that would mean itself); it reaches the host via
                           "host.docker.internal" instead (see
                           docker-compose.selenium.yml for the extra_hosts
                           entry that makes that resolve, on both Docker
                           Desktop and Linux/CI). If BASE_URL does not point
                           at localhost/127.0.0.1 (e.g. it is already a
                           routable CI hostname), the two are the same and no
                           rewriting happens.

`tests/e2e` is run as its own pytest invocation, separate from
`tests/content`/`tests/unit` (see tests/README.md), so `tests/content` is not
on `sys.path` by default here. It is added below, once, so
`test_link_crawler.py` can share `tests/content/link_report.py`'s broken-link
report formatter instead of duplicating it.
'''

from __future__ import annotations

import os
import sys
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'content'))

BASE_URL = os.environ.get('E2E_BASE_URL', 'http://localhost:8082').rstrip('/')
SELENIUM_REMOTE_URL = os.environ.get(
    'SELENIUM_REMOTE_URL', 'http://localhost:4444/wd/hub'
)


def _default_browser_base_url(base_url: str) -> str:
    parts = urlsplit(base_url)
    if parts.hostname in ('localhost', '127.0.0.1'):
        new_netloc = 'host.docker.internal'
        if parts.port:
            new_netloc += f':{parts.port}'
        return urlunsplit((parts.scheme, new_netloc, parts.path, parts.query, parts.fragment))
    return base_url


BROWSER_BASE_URL = os.environ.get(
    'E2E_BROWSER_BASE_URL', _default_browser_base_url(BASE_URL)
).rstrip('/')


@pytest.fixture(scope='session', name='base_url')
def _base_url_fixture() -> str:
    '''Where pytest itself (running on the host) reaches the site, for plain HTTP checks.'''
    return BASE_URL


@pytest.fixture(scope='session', name='browser_base_url')
def _browser_base_url_fixture() -> str:
    '''Where the browser, running inside the selenium container, reaches the site.'''
    return BROWSER_BASE_URL


@pytest.fixture(scope='session', name='driver')
def _driver_fixture() -> Iterator[WebDriver]:
    '''
    A single Remote WebDriver session shared across the whole test session,
    talking to the selenium/standalone-chrome container over the W3C
    WebDriver wire protocol. No local chromedriver or browser install needed.
    '''
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,1024')

    remote_driver = WebDriver(command_executor=SELENIUM_REMOTE_URL, options=options)
    remote_driver.set_page_load_timeout(30)
    try:
        yield remote_driver
    finally:
        remote_driver.quit()


@pytest.fixture
def visit(driver: WebDriver, browser_base_url: str):
    '''Navigate the shared driver to a path under browser_base_url and return the driver.'''

    def _visit(path: str) -> WebDriver:
        url = path if path.startswith('http') else f'{browser_base_url}{path}'
        driver.get(url)
        return driver

    return _visit
