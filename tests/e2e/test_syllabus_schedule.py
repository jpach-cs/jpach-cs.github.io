'''
Layer 2 check (g): syllabus and schedule pages for each course render.

These pages are Jekyll pages built from `syllabus.md` / `schedule.md` with no
permalink override, so Jekyll's default output path is `<name>.html` -- the
course index pages link to them *without* that extension (a separate, real
bug caught by test_link_crawler.py / test_home_and_nav.py's sibling checks).
This test hits the actual working URLs directly, the way test (g) is meant to
be read: does the syllabus/schedule content itself render correctly, in
isolation from whether the site's nav links happen to reach it.

"Renders" is checked with the same real-browser + heading-substring approach
as the course pages, plus a soft-404 sweep.

Known real defect this catches: teaching/csci-446/schedule.html and
teaching/esof-322/schedule.html both render the heading "Course Schedule --
CSCI 232" (copy-pasted from csci-232/schedule.md and never updated), instead
of their own course code.
'''

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from soft_404 import looks_like_soft_404

# course -> expected course-code substring in the page's own <h1>
COURSES = {
    'csci-112': 'CSCI 112',
    'csci-232': 'CSCI 232',
    'csci-446': 'CSCI 446',
    'esof-322': 'ESOF 322',
}


def _own_heading_text(driver: WebDriver) -> list[str]:
    '''All <h1> text on the page except the site-wide header ("Jacob L. Pach").'''
    return [h.text for h in driver.find_elements(By.CSS_SELECTOR, 'h1') if 'Jacob L. Pach' not in h.text]


def test_syllabus_pages_render_with_correct_course_code(visit) -> None:
    '''Each course's syllabus.html must render a heading with its own course code.'''
    failures = []
    for course, expected in COURSES.items():
        driver: WebDriver = visit(f'/teaching/{course}/syllabus.html')
        headings = _own_heading_text(driver)
        if not any(expected in h for h in headings):
            failures.append(f'{course}: expected "{expected}" in heading, found {headings}')
        soft_404 = looks_like_soft_404(driver.page_source)
        if soft_404:
            failures.append(f'{course} syllabus looks like a soft 404 ("{soft_404}")')
    assert not failures, 'Syllabus page issue(s):\n' + '\n'.join(failures)


def test_schedule_pages_render_with_correct_course_code(visit) -> None:
    '''Each course's schedule.html must render a heading with its own course code.'''
    failures = []
    for course, expected in COURSES.items():
        driver: WebDriver = visit(f'/teaching/{course}/schedule.html')
        headings = _own_heading_text(driver)
        if not any(expected in h for h in headings):
            failures.append(f'{course}: expected "{expected}" in heading, found {headings}')
        soft_404 = looks_like_soft_404(driver.page_source)
        if soft_404:
            failures.append(f'{course} schedule looks like a soft 404 ("{soft_404}")')
    assert not failures, 'Schedule page issue(s):\n' + '\n'.join(failures)
