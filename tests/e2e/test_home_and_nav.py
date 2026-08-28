'''
Layer 2 check (e): home page loads, has a non-empty title, and the nav links
work.

"Work" is checked the way a real visitor would notice it fail: click the link
in a real browser and see whether you land on a real page or a 404. This does
not need HTTP status codes (see crawler.py for why the exhaustive link check
uses `requests` instead) -- nginx's default error page has a distinctive
title ("404 Not Found"), so a plain Selenium click-and-inspect is enough here.

Known real defect this catches: the home page's "Research" link
(href="/research/") 404s. There is no research page on the site.
'''

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

# The home page's primary section links, keyed by visible link text.
PRIMARY_NAV_LINKS = {
    'About & Portfolio': '/portfolio/',
    'Research': '/research/',
    'Teaching': '/teaching/',
    'Downloads & Toolchains': '/downloads/',
}


def test_home_page_loads_with_non_empty_title(visit) -> None:
    '''The home page must load with a real, non-empty, non-error <title>.'''
    driver: WebDriver = visit('/')
    assert driver.title.strip(), 'Home page <title> is empty'
    assert '404' not in driver.title, f'Home page title looks like an error page: {driver.title!r}'


def test_home_page_nav_links_are_present(visit) -> None:
    '''Each expected primary nav link must appear somewhere on the home page.'''
    driver: WebDriver = visit('/')
    hrefs = {a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')}
    for label, path in PRIMARY_NAV_LINKS.items():
        full_urls = {h for h in hrefs if h and h.rstrip('/').endswith(path.rstrip('/'))}
        assert full_urls, f'Expected a nav link to {path} ("{label}") on the home page'


def test_each_home_page_nav_link_navigates_successfully(visit) -> None:
    '''Navigating directly to each primary nav link's target must land on a real page.'''
    failures = []
    for label, path in PRIMARY_NAV_LINKS.items():
        driver: WebDriver = visit(path)
        title = driver.title.strip()
        if not title or '404' in title or 'not found' in title.lower():
            failures.append(f'{label} ({path}) -> title={title!r}')
    assert not failures, 'Nav link(s) do not lead to a real page:\n' + '\n'.join(
        f'  {f}' for f in failures
    )


def test_teaching_nav_link_click_lands_on_teaching_page(visit) -> None:
    '''An actual click-through, not just a direct navigation, to exercise the real link.'''
    driver: WebDriver = visit('/')
    teaching_link = driver.find_element(By.CSS_SELECTOR, 'a[href="/teaching/"]')
    teaching_link.click()
    assert driver.current_url.rstrip('/').endswith('/teaching')
    heading = driver.find_element(By.CSS_SELECTOR, 'h1#teaching')
    assert heading.text.strip().lower() == 'teaching'
