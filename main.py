"""Main entry point for TTT AI application."""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from ttt_ai.play import main

if __name__ == "__main__":
    main()
