'''
Layer 1 content check: lecture decks must be branded for the course they live
under, and must not ship placeholder outlines.

Both checks read the deck's extracted text with `pdftotext`, so they are
skipped (not failed) when poppler-utils is not installed -- see
`tests/README.md` for how to install it.

Known real defects these catch today:
  * teaching/csci-232/lectures/lecture02/index.pdf is branded "CSCI 112 /
    Programming with C" even though it lives under csci-232.
  * teaching/csci-446/lectures/lecture02/index.pdf has the same "CSCI 112"
    mislabel.
  * Both of those same two decks have an "OUTLINE:" section that is just "??"
    instead of real content.

The course-code check is scoped to *lecture* decks only. Labs and assignments
(e.g. the Git and command-line labs) are intentionally reused verbatim across
all four courses and keep their original "CSCI 112" branding by design -- that
is not a mislabel, it is shared boilerplate, so checking it would just be
noise. Lecture decks are expected to be course-specific, which is why a
mismatch there is a real defect.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest

from course_codes import course_code_from_path, first_course_code_in_text
from pdf_text import PDFTOTEXT_AVAILABLE, PdfTextError, extract_text
from repo import TEACHING_ROOT

# A line consisting of only "??" (optionally surrounded by whitespace). Scoped
# to a whole line so we do not false-positive on legitimate uses of "??" inside
# a sentence, e.g. "?? -- Untracked file (not added to Git yet)" in the Git lab.
PLACEHOLDER_LINE = re.compile(r'(?m)^\s*\?\?\s*$')


def discover_lecture_decks() -> list[Path]:
    '''Return every lecture deck PDF under the teaching tree, sorted for stable test IDs.'''
    return sorted(TEACHING_ROOT.glob('*/lectures/*/index.pdf'))


LECTURE_DECKS = discover_lecture_decks()
DECK_IDS = [str(p.relative_to(TEACHING_ROOT)) for p in LECTURE_DECKS]


def _require_pdftotext() -> None:
    if not PDFTOTEXT_AVAILABLE:
        pytest.skip('pdftotext (poppler-utils) is not installed; see tests/README.md')


def test_lecture_decks_were_discovered() -> None:
    '''Sanity check: fail loudly if the glob above stops finding anything.'''
    assert LECTURE_DECKS, f'No lecture decks found under {TEACHING_ROOT}'


@pytest.mark.parametrize('deck_path', LECTURE_DECKS, ids=DECK_IDS)
def test_deck_is_branded_for_its_own_course(deck_path: Path) -> None:
    '''A lecture deck's extracted text must name its own course code.'''
    _require_pdftotext()
    expected = course_code_from_path(deck_path, TEACHING_ROOT)
    try:
        text = extract_text(deck_path)
    except PdfTextError as exc:
        pytest.fail(f'Could not extract text from {deck_path}: {exc}')
    actual = first_course_code_in_text(text)
    assert actual == expected, (
        f'{deck_path.relative_to(TEACHING_ROOT)} is branded "{actual}" '
        f'but lives under the "{expected}" course directory.'
    )


@pytest.mark.parametrize('deck_path', LECTURE_DECKS, ids=DECK_IDS)
def test_deck_has_no_placeholder_outline(deck_path: Path) -> None:
    '''A lecture deck's outline must be real content, not a "??" placeholder.'''
    _require_pdftotext()
    try:
        text = extract_text(deck_path)
    except PdfTextError as exc:
        pytest.fail(f'Could not extract text from {deck_path}: {exc}')
    match = PLACEHOLDER_LINE.search(text)
    assert match is None, (
        f'{deck_path.relative_to(TEACHING_ROOT)} contains a placeholder "??" line '
        f'where real slide content should be.'
    )
