'''
Layer 1 content check: every local link in each `teaching/**/index.md` must
resolve to a file that actually exists in the source tree.

As of writing, the index pages advertise Lectures 01-15 and Labs 01-15 for
every course while only a couple of each actually exist, so this test fails
today with a few hundred broken links. That is by design: the site's content
is genuinely incomplete, and this test is meant to stay red -- and readable --
until that content is filled in, rather than papering over it with an
allowlist that would need constant upkeep and would silently stop meaning
anything the moment it drifted from reality.
'''

from __future__ import annotations

import re
from collections import defaultdict

from link_report import format_broken_links_report
from link_resolver import resolve_link
from repo import REPO_ROOT, TEACHING_ROOT

LINK_PATTERN = re.compile(r"\{\{ '([^']+)' \| relative_url \}\}")


def _find_broken_links() -> set[tuple[str, str]]:
    '''Return the set of (source page, link) pairs whose link does not resolve.'''
    broken: set[tuple[str, str]] = set()
    for md_file in sorted(TEACHING_ROOT.glob('*/index.md')):
        text = md_file.read_text(encoding='utf-8')
        for link in LINK_PATTERN.findall(text):
            if resolve_link(link, REPO_ROOT) is None:
                broken.add((str(md_file.relative_to(REPO_ROOT)), link))
    return broken


def _format_broken(broken: set[tuple[str, str]]) -> str:
    '''Group broken (source, link) pairs by source page and format a report.'''
    by_source: dict[str, list[str]] = defaultdict(list)
    for source, link in broken:
        by_source[source].append(link)
    header = f'{len(broken)} broken local link(s) in teaching/**/index.md:'
    return format_broken_links_report(header, dict(by_source))


def test_index_pages_were_discovered() -> None:
    '''Sanity check: fail loudly if the glob above stops finding anything.'''
    assert list(TEACHING_ROOT.glob('*/index.md')), (
        f'No teaching/*/index.md files found under {TEACHING_ROOT}'
    )


def test_no_broken_links() -> None:
    '''Every local link in teaching/**/index.md must resolve to a real file.'''
    broken = _find_broken_links()
    assert not broken, _format_broken(broken)
