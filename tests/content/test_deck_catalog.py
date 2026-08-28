'''
Layer 1 content check: `_data/decks.yml` and the deck directories on disk
describe the same set of decks.

The course index pages used to hand-maintain four near-identical lists of
"Lecture 01" through "Lecture 15" and "Lab 01" through "Lab 15" regardless of
what had actually been written, which is how they came to advertise a few
hundred links to directories that do not exist. They now render from the
catalog in `_data/decks.yml` through `_includes/deck-lists.html`, and this
file is what keeps that catalog honest: a deck directory that is not listed,
a listed deck with no directory, or a `source` that disagrees with what is in
the directory all fail here rather than shipping as a dead link.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from repo import GIT_AVAILABLE, REPO_ROOT, TEACHING_ROOT, tracked_files

CATALOG_PATH = REPO_ROOT / '_data' / 'decks.yml'

# Matches the deck directory names the site uses: "lecture05", "lecture01-intro",
# "lab03", "ass01". The label a deck carries has to agree with this.
DIR_PATTERN = re.compile(r'^(lecture|lab|ass)(\d{2})(?:-(\w+))?$')

# How a deck directory's numeric prefix spells itself in the catalog's `label`.
LABEL_PREFIX = {'lecture': 'Lecture', 'lab': 'Lab', 'ass': 'Assignment'}


def load_catalog() -> dict:
    '''Read _data/decks.yml, the single source the course index pages render from.'''
    return yaml.safe_load(CATALOG_PATH.read_text(encoding='utf-8'))


CATALOG = load_catalog()
SECTION_DIRS = [section['dir'] for section in CATALOG['sections']]


def catalog_entries() -> list[tuple[str, str, dict]]:
    '''Return every (course, section, deck) triple listed in the catalog.'''
    entries = []
    for course, sections in CATALOG['courses'].items():
        for section, decks in sections.items():
            for deck in decks:
                entries.append((course, section, deck))
    return entries


def holds_a_deck(deck_dir: Path, tracked: set[str]) -> bool:
    '''
    Return whether a directory actually holds something publishable: either a
    Marp source, or an `index.html` committed before the render pipeline
    existed. `teaching/csci-232/assignments/ass01/` holds neither - only a
    six-byte file named `index.pdf` that is not a PDF - so it is not a deck
    the catalog can name, and it is left to `test_pdf_integrity.py` to report.
    '''
    if (deck_dir / 'slides.md').is_file():
        return True
    return (deck_dir / 'index.html').relative_to(REPO_ROOT).as_posix() in tracked


def deck_directories() -> list[Path]:
    '''
    Return every deck directory on disk: `teaching/<course>/<section>/<deck>`
    for the sections the site publishes, skipping directories that hold no
    publishable deck.
    '''
    tracked = tracked_files() if GIT_AVAILABLE else set()
    found = []
    for course_dir in sorted(TEACHING_ROOT.iterdir()):
        if not course_dir.is_dir():
            continue
        for section in SECTION_DIRS:
            section_dir = course_dir / section
            if not section_dir.is_dir():
                continue
            found.extend(
                deck_dir for deck_dir in sorted(section_dir.iterdir())
                if deck_dir.is_dir() and holds_a_deck(deck_dir, tracked)
            )
    return found


ENTRIES = catalog_entries()
ENTRY_IDS = [f'{course}/{section}/{deck["dir"]}' for course, section, deck in ENTRIES]


def test_catalog_lists_decks() -> None:
    '''Sanity check: fail loudly if the catalog is empty or unreadable.'''
    assert ENTRIES, f'{CATALOG_PATH.relative_to(REPO_ROOT)} lists no decks'


def test_every_deck_directory_is_in_the_catalog() -> None:
    '''No deck may exist on disk without a name and a link on its course page.'''
    on_disk = {
        deck_dir.relative_to(TEACHING_ROOT).as_posix() for deck_dir in deck_directories()
    }
    listed = {f'{course}/{section}/{deck["dir"]}' for course, section, deck in ENTRIES}
    missing = sorted(on_disk - listed)
    assert not missing, (
        f'{len(missing)} deck director(ies) exist under teaching/ but are not listed in '
        f'{CATALOG_PATH.relative_to(REPO_ROOT)}, so no course page links to them:\n  '
        + '\n  '.join(missing)
    )


@pytest.mark.parametrize(('course', 'section', 'deck'), ENTRIES, ids=ENTRY_IDS)
def test_catalog_entry_has_a_directory(course: str, section: str, deck: dict) -> None:
    '''Every catalog entry must point at a directory that exists.'''
    deck_dir = TEACHING_ROOT / course / section / deck['dir']
    assert deck_dir.is_dir(), (
        f'{CATALOG_PATH.relative_to(REPO_ROOT)} lists {course}/{section}/{deck["dir"]}, '
        f'but {deck_dir.relative_to(REPO_ROOT)} does not exist. The course page would '
        f'render a dead link.'
    )


@pytest.mark.parametrize(('course', 'section', 'deck'), ENTRIES, ids=ENTRY_IDS)
def test_catalog_entry_is_fully_described(course: str, section: str, deck: dict) -> None:
    '''Each entry needs a label and a title; a nameless deck is what this replaced.'''
    where = f'{course}/{section}/{deck.get("dir", "?")}'
    for field in ('dir', 'label', 'title', 'source'):
        assert deck.get(field), f'{where} is missing a non-empty "{field}".'
    assert deck['source'] in ('slides', 'legacy'), (
        f'{where} has source "{deck["source"]}"; expected "slides" or "legacy".'
    )


@pytest.mark.parametrize(('course', 'section', 'deck'), ENTRIES, ids=ENTRY_IDS)
def test_label_matches_directory_name(course: str, section: str, deck: dict) -> None:
    '''
    A deck labelled "Lecture 05" must live in a directory called "lecture05", so
    the visible numbering and the URL can never drift apart.
    '''
    match = DIR_PATTERN.match(deck['dir'])
    assert match, (
        f'{course}/{section}/{deck["dir"]}: directory name does not follow the '
        f'"lecture05" / "lab03" / "ass01" convention.'
    )
    kind, number, suffix = match.groups()
    if suffix:
        # A suffixed directory such as "lecture01-intro" sits outside the numbered
        # run and carries a descriptive label instead, e.g. "Course Introduction".
        return
    expected = f'{LABEL_PREFIX[kind]} {number}'
    assert deck['label'] == expected, (
        f'{course}/{section}/{deck["dir"]} is labelled "{deck["label"]}"; its directory '
        f'name says it should be "{expected}".'
    )


@pytest.mark.skipif(not GIT_AVAILABLE, reason='git is not installed')
@pytest.mark.parametrize(('course', 'section', 'deck'), ENTRIES, ids=ENTRY_IDS)
def test_source_matches_the_directory_contents(course: str, section: str, deck: dict) -> None:
    '''
    `source` decides which formats the course page offers, so it has to match
    reality: a "slides" deck is rendered from a tracked `slides.md` and gets an
    HTML, PDF and Markdown link; a "legacy" deck has no source and only the
    `index.html` committed before the render pipeline existed.
    '''
    deck_dir = TEACHING_ROOT / course / section / deck['dir']
    slides = deck_dir / 'slides.md'
    if deck['source'] == 'slides':
        assert slides.is_file(), (
            f'{course}/{section}/{deck["dir"]} is catalogued as source "slides", but '
            f'{slides.relative_to(REPO_ROOT)} does not exist, so the Markdown link on '
            f'the course page would be dead.'
        )
        return
    assert not slides.is_file(), (
        f'{course}/{section}/{deck["dir"]} is catalogued as source "legacy", but it has '
        f'a {slides.relative_to(REPO_ROOT)} source. Change its source to "slides" so the '
        f'course page links the Markdown too.'
    )
    index_html = (deck_dir / 'index.html').relative_to(REPO_ROOT).as_posix()
    assert index_html in tracked_files(), (
        f'{course}/{section}/{deck["dir"]} is catalogued as source "legacy", but '
        f'{index_html} is not committed, so nothing would be published there.'
    )
