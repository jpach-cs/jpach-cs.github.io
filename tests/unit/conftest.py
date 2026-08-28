'''
Make tools/ importable so the unit tests can `import pptx2marp` without the
package being installed, from any checkout location.
'''

import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[2] / 'tools'
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
