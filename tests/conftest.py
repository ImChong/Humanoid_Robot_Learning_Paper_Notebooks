"""Shared pytest configuration: add the project root to ``sys.path``.

Allows ``from scripts.<module> import ...`` from any test file without each
test having to do its own ``sys.path`` dance.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
