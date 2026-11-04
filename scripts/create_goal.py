#!/usr/bin/env python3
"""Render a complete new roadmap from structured JSON on standard input."""

import sys

sys.dont_write_bytecode = True
from project_state import main


if __name__ == "__main__":
    raise SystemExit(main("create"))
