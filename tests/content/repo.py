'''
Shared helpers for locating repository content.

Every Layer 1 (content integrity) test operates directly on the working tree, so
the only thing these tests need from the environment is a path to the repo root.
No network access, no Docker, no built site required.
'''

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def find_repo_root() -> Path:
    '''
    Walk upward from this file until a directory containing `_config.yml` is
    found. That file marks the Jekyll site root. Avoids any hardcoded absolute
    path so the suite works from any checkout location, including CI runners.
    '''
    here = Path(__file__).resolve()
    for candidate in [here.parent, *here.parents]:
        if (candidate / '_config.yml').exists():
            return candidate
    raise RuntimeError(
        f'Could not locate repo root (a directory with _config.yml) above {here}'
    )


REPO_ROOT = find_repo_root()
TEACHING_ROOT = REPO_ROOT / 'teaching'

# Whether `git` is on PATH. Checks that need the index skip themselves without
# it, so the suite still runs from an exported tarball.
GIT_AVAILABLE = shutil.which('git') is not None


def tracked_files() -> set[str]:
    '''
    Return every path `git` currently tracks in the index, as POSIX paths
    relative to the repo root. Used to tell content committed to the repo
    apart from build output that merely happens to be present on disk.
    '''
    result = subprocess.run(
        ['git', 'ls-files'],
        cwd=REPO_ROOT,
        capture_output=True,
        check=True,
        text=True,
    )
    return set(result.stdout.splitlines())
