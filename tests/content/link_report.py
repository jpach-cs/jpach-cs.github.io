'''
Shared "broken links" report formatting.

Both the Layer 1 source-tree check (`test_index_links.py`) and the Layer 2
live-crawl check (`tests/e2e/test_link_crawler.py`) find broken links, group
them by the page that linked to them, and print an indented, readable report
as the assertion failure message. That grouping/formatting logic is identical
in both places, so it lives here once instead of twice.

`tests/e2e` is invoked as its own pytest run (see tests/README.md), separate
from `tests/content`/`tests/unit`, so `tests/content` is not automatically on
`sys.path` when the e2e suite runs. `tests/e2e/conftest.py` adds it
explicitly, once, at import time, so `test_link_crawler.py` can import this
module the same way `test_index_links.py` does.
'''

from __future__ import annotations


def format_broken_links_report(header: str, by_source: dict[str, list[str]]) -> str:
    '''
    Render a "broken links grouped by source page" report.

    `header` is the first line of the report (typically a count summary).
    `by_source` maps each source page to the broken links found on it. The
    source pages are sorted for stable output; the links under each source
    are sorted too.
    '''
    lines = [header, '']
    for source, links in sorted(by_source.items()):
        lines.append(f'{source} ({len(links)} broken link(s)):')
        for link in sorted(links):
            lines.append(f'  {link}')
        lines.append('')
    return '\n'.join(lines)
