'''
Layer 1 content check (bonus, beyond the original ticket): the per-course
`syllabus.md` and `schedule.md` pages must actually be about their own course.

These were not in the original list of checks to build, but turned up while
exercising the site for the E2E layer and are the same species of bug as the
PDF branding mismatch, just in markdown instead of PDF, and just as cheap to
catch with pure file inspection. Keeping them in a separate module so it is
clear they are additional coverage, not part of the originally specified
checks (a)-(d).

Known real defects these catch today:
  * teaching/csci-446/schedule.md and teaching/esof-322/schedule.md both have
    the heading "Course Schedule -- CSCI 232" (copy-pasted from
    teaching/csci-232/schedule.md and never updated) and their "Back to ..."
    link also points at csci-232.
  * teaching/esof-322/syllabus.md has a "Back to ESOF 322" link that actually
    points at /teaching/csci-446/.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest

from course_codes import course_code_from_path, first_course_code_in_text
from repo import TEACHING_ROOT

HEADING_PATTERN = re.compile(r'(?m)^#\s+(.+)$')
BACK_LINK_PATTERN = re.compile(
    r"\[←\s*Back to[^\]]*\]\(\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}\)"
)


def discover_course_pages(filename: str) -> list[Path]:
    '''Return every per-course `filename` (e.g. "syllabus.md") under the teaching tree.'''
    return sorted(TEACHING_ROOT.glob(f'*/{filename}'))


SYLLABUS_PAGES = discover_course_pages('syllabus.md')
SCHEDULE_PAGES = discover_course_pages('schedule.md')

SYLLABUS_IDS = [str(p.relative_to(TEACHING_ROOT)) for p in SYLLABUS_PAGES]
SCHEDULE_IDS = [str(p.relative_to(TEACHING_ROOT)) for p in SCHEDULE_PAGES]


def _course_dir_url(page_path: Path, teaching_root: Path) -> str:
    course_dir = page_path.resolve().relative_to(teaching_root.resolve()).parts[0]
    return f'/teaching/{course_dir}/'


def test_syllabus_and_schedule_pages_were_discovered() -> None:
    '''Sanity check: fail loudly if the globs above stop finding anything.'''
    assert SYLLABUS_PAGES, f'No syllabus.md files found under {TEACHING_ROOT}'
    assert SCHEDULE_PAGES, f'No schedule.md files found under {TEACHING_ROOT}'


@pytest.mark.parametrize('page_path', SCHEDULE_PAGES, ids=SCHEDULE_IDS)
def test_schedule_heading_matches_its_own_course(page_path: Path) -> None:
    '''A schedule page's top-level heading must name its own course code.'''
    expected = course_code_from_path(page_path, TEACHING_ROOT)
    text = page_path.read_text(encoding='utf-8')
    match = HEADING_PATTERN.search(text)
    assert match is not None, f'{page_path} has no top-level "# ..." heading'
    actual = first_course_code_in_text(match.group(1))
    assert actual == expected, (
        f'{page_path.relative_to(TEACHING_ROOT)} heading is "{match.group(1).strip()}" '
        f'(course code "{actual}") but lives under the "{expected}" course directory.'
    )


@pytest.mark.parametrize('page_path', SYLLABUS_PAGES, ids=SYLLABUS_IDS)
def test_syllabus_heading_matches_its_own_course(page_path: Path) -> None:
    '''A syllabus page's top-level heading must name its own course code.'''
    expected = course_code_from_path(page_path, TEACHING_ROOT)
    text = page_path.read_text(encoding='utf-8')
    match = HEADING_PATTERN.search(text)
    assert match is not None, f'{page_path} has no top-level "# ..." heading'
    actual = first_course_code_in_text(match.group(1))
    assert actual == expected, (
        f'{page_path.relative_to(TEACHING_ROOT)} heading is "{match.group(1).strip()}" '
        f'(course code "{actual}") but lives under the "{expected}" course directory.'
    )


@pytest.mark.parametrize(
    'page_path', SYLLABUS_PAGES + SCHEDULE_PAGES,
    ids=SYLLABUS_IDS + SCHEDULE_IDS,
)
def test_back_link_points_at_its_own_course(page_path: Path) -> None:
    '''A page's "Back to ..." link must point at its own course directory.'''
    expected_url = _course_dir_url(page_path, TEACHING_ROOT)
    text = page_path.read_text(encoding='utf-8')
    match = BACK_LINK_PATTERN.search(text)
    assert match is not None, f'{page_path} has no "[<- Back to ...]" link'
    actual_url = match.group(1)
    assert actual_url == expected_url, (
        f'{page_path.relative_to(TEACHING_ROOT)} has a back-link to "{actual_url}" '
        f'but should point back at its own course, "{expected_url}".'
    )
