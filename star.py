#!/usr/bin/env python3
"""
Star Programming Language CLI Entrypoint
"""

import sys

# Configure UTF-8 encoding on standard streams to avoid Windows charmap issues
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from star_engine.cli import main

if __name__ == "__main__":
    sys.exit(main())
