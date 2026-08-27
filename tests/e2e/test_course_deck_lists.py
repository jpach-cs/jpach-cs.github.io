'''
Layer 2 check: each course page renders its deck list from the catalog, and
every link in that list resolves.

`tests/content/test_deck_catalog.py` already holds `_data/decks.yml` and the
directories on disk to each other. What it cannot see is whether Jekyll
actually rendered the list: an include that fails to resolve, a Liquid typo,
or a `_data` file the build never picked up would all leave a course page
silently missing its decks while every Layer 1 check still passed. This is
the check that the names and links reached the published page.
'''

from __future__ import annotations

from pathlib import Path

import pytest
import requests
import yaml

CATALOG = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / '_data' / 'decks.yml').read_text(encoding='utf-8')
)

COURSES = sorted(CATALOG['courses'])
SECTION_DIRS = [section['dir'] for section in CATALOG['sections']]

# How many decks a `source` value is published in, and under which filenames.
FORMAT_FILES = {
    'slides': ('', 'index.pdf', 'slides.md'),
    'legacy': ('', 'index.pdf'),
}


def course_decks(course: str) -> list[tuple[str, dict]]:
    '''Return every (section, deck) pair the catalog lists for one course.'''
    sections = CATALOG['courses'][course]
    return [
        (section, deck)
        for section in SECTION_DIRS
        for deck in sections.get(section, [])
    ]


@pytest.mark.parametrize('course', COURSES)
def test_course_page_names_every_deck(base_url: str, course: str) -> None:
    '''Every catalogued deck's title must appear on its course page.'''
    page = requests.get(f'{base_url}/teaching/{course}/', timeout=15)
    assert page.status_code == 200, f'/teaching/{course}/ -> {page.status_code}'
    missing = [
        f'{section}/{deck["dir"]}: {deck["title"]}'
        for section, deck in course_decks(course)
        if deck['title'] not in page.text
    ]
    assert not missing, (
        f'{len(missing)} deck title(s) from _data/decks.yml are not rendered on '
        f'/teaching/{course}/:\n  ' + '\n  '.join(missing)
    )


@pytest.mark.parametrize('course', COURSES)
def test_every_advertised_deck_format_is_served(base_url: str, course: str) -> None:
    '''Each format a course page offers for a deck must actually be served.'''
    failures = []
    for section, deck in course_decks(course):
        base = f'{base_url}/teaching/{course}/{section}/{deck["dir"]}/'
        for name in FORMAT_FILES[deck['source']]:
            status = requests.get(f'{base}{name}', timeout=30).status_code
            if status != 200:
                failures.append(f'{base}{name} -> {status}')
    assert not failures, (
        f'{len(failures)} advertised deck link(s) on /teaching/{course}/ did not '
        f'return 200:\n  ' + '\n  '.join(failures)
    )
