#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path("/home/cozwood/Documents/Dev/the_way_of_scripture")


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    completed = subprocess.run(cmd, cwd=ROOT)
    return completed.returncode


def main() -> int:
    commands = [
        ["python3", "-m", "py_compile", "tools/generate_study_pages.py"],
        ["python3", "-m", "py_compile", "tools/validate_passages.py"],
        ["python3", "tools/validate_passages.py"],
    ]
    for cmd in commands:
        code = run(cmd)
        if code != 0:
            return code
    print("Repo checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
