#!/usr/bin/env python3
"""Archive a completed/cancelled goal and prepare the next goal in one command."""

import sys

sys.dont_write_bytecode = True
from project_state import main


if __name__ == "__main__":
    raise SystemExit(main("archive"))
