'''
Layer 1 content check: every PDF shipped in the site must actually be a PDF.

This is pure file inspection (magic bytes + size floor), no external tools
required, so it runs everywhere pytest runs.

Known real defect this catches today: `teaching/csci-232/assignments/ass01/index.pdf`
is a 6-byte file (a UTF-16LE byte-order-mark plus a CRLF) that was saved instead
of the real assignment PDF.
'''

from __future__ import annotations

from pathlib import Path

import pytest

from repo import TEACHING_ROOT

PDF_MAGIC = b'%PDF-'

# A real slide deck or assignment PDF produced by this site's toolchain is at
# minimum tens of kilobytes. 1 KiB is a generous floor: comfortably above a
# corrupt placeholder file, comfortably below the smallest legitimate PDF.
MIN_PDF_SIZE_BYTES = 1024


def discover_pdfs() -> list[Path]:
    '''Return every PDF under the teaching content tree, sorted for stable test IDs.'''
    return sorted(TEACHING_ROOT.rglob('*.pdf'))


PDF_FILES = discover_pdfs()
PDF_IDS = [str(p.relative_to(TEACHING_ROOT)) for p in PDF_FILES]


def test_pdfs_were_discovered() -> None:
    '''Sanity check: fail loudly if the glob above stops finding anything.'''
    assert PDF_FILES, f'No PDF files found under {TEACHING_ROOT}'


@pytest.mark.parametrize('pdf_path', PDF_FILES, ids=PDF_IDS)
def test_pdf_has_minimum_size(pdf_path: Path) -> None:
    '''A real PDF from this site's toolchain is far larger than a corrupt placeholder.'''
    size = pdf_path.stat().st_size
    assert size >= MIN_PDF_SIZE_BYTES, (
        f'{pdf_path.relative_to(TEACHING_ROOT)} is only {size} bytes '
        f'(minimum expected: {MIN_PDF_SIZE_BYTES}). This looks like a placeholder '
        f'or a corrupted save, not a real PDF.'
    )


@pytest.mark.parametrize('pdf_path', PDF_FILES, ids=PDF_IDS)
def test_pdf_has_valid_magic_bytes(pdf_path: Path) -> None:
    '''A real PDF starts with the "%PDF-" magic bytes.'''
    with pdf_path.open('rb') as handle:
        header = handle.read(len(PDF_MAGIC))
    assert header == PDF_MAGIC, (
        f'{pdf_path.relative_to(TEACHING_ROOT)} does not start with the PDF magic '
        f'bytes {PDF_MAGIC!r}; found {header!r} instead. This file is not a real PDF.'
    )
