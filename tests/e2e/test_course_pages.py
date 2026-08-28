'''
Layer 2 check (f): each of the 4 course pages returns 200 and renders its
course heading.

The "returns 200" half is a plain HTTP check (see crawler.py's module
docstring for why status codes are checked with `requests` rather than
through the WebDriver). The "renders its course heading" half drives the real
browser and reads the rendered DOM, which is the part Selenium is for.
'''

from __future__ import annotations

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

# course path -> substring expected in the page's <h1>
COURSE_PAGES = {
    '/teaching/csci-112/': 'CSCI 112',
    '/teaching/csci-232/': 'CSCI 232',
    '/teaching/csci-446/': 'CSCI 446',
    '/teaching/esof-322/': 'ESOF 322',
}


def test_course_page_returns_200(base_url: str) -> None:
    '''Each of the 4 course pages must return HTTP 200.'''
    failures = []
    for path in COURSE_PAGES:
        response = requests.get(f'{base_url}{path}', timeout=15)
        if response.status_code != 200:
            failures.append(f'{path} -> {response.status_code}')
    assert not failures, 'Course page(s) did not return 200:\n' + '\n'.join(failures)


def test_course_page_renders_its_own_heading(visit) -> None:
    '''Each of the 4 course pages must render an <h1> containing its own course code.'''
    failures = []
    for path, expected_substring in COURSE_PAGES.items():
        driver: WebDriver = visit(path)
        headings = driver.find_elements(By.CSS_SELECTOR, 'h1')
        # The site header itself contributes an <h1> ("Jacob L. Pach"); the
        # course heading is the page's own content heading, further down.
        matching = [h for h in headings if expected_substring in h.text]
        if not matching:
            all_text = [h.text for h in headings]
            failures.append(f'{path}: expected an <h1> containing "{expected_substring}", '
                             f'found {all_text}')
    assert not failures, 'Course page heading mismatch(es):\n' + '\n'.join(failures)
