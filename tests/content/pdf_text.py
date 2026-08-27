'''
Thin wrapper around the `pdftotext` binary (from poppler-utils).

Tests that need to inspect PDF *content* (branding, placeholder outlines) go
through here so there is exactly one place that knows how to shell out, and
exactly one place that decides what happens when `pdftotext` is not installed.
'''

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

PDFTOTEXT_AVAILABLE = shutil.which('pdftotext') is not None


class PdfTextError(RuntimeError):
    '''Raised when `pdftotext` is unavailable or fails to extract text.'''


def extract_text(pdf_path: Path, timeout: float = 30.0) -> str:
    '''
    Return the plain-text contents of a PDF, extracted with `pdftotext -layout`
    so multi-column slide text does not get interleaved. Raises PdfTextError if
    the tool is missing or the extraction fails (e.g. the file is not really a
    PDF at all).
    '''
    if not PDFTOTEXT_AVAILABLE:
        raise PdfTextError(
            'pdftotext is not installed (poppler-utils). '
            'Install it to run content-based PDF checks, e.g. '
            '`apt-get install poppler-utils` or `brew install poppler`.'
        )
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', str(pdf_path), '-'],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise PdfTextError(f'pdftotext timed out on {pdf_path}') from exc
    if result.returncode != 0:
        raise PdfTextError(
            f'pdftotext failed on {pdf_path} (exit {result.returncode}): {result.stderr.strip()}'
        )
    return result.stdout
