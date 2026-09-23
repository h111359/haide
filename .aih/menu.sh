#!/bin/sh
if command -v python3 >/dev/null 2>&1; then
    exec python3 -B "$(dirname "$0")/engine/cli.py" menu "$@"
fi
echo "AIH requires Python 3.11 or newer. Install Python, then run python3 -B .aih/engine/cli.py menu." >&2
exit 1
