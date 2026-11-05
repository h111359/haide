#!/usr/bin/env python3
"""HAI runtime entry point."""
import sys
sys.dont_write_bytecode = True
from runtime.cli import main
if __name__ == '__main__':
    raise SystemExit(main())
