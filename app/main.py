import sys
import os

# Ensure the root directory is on the path so absolute imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.bootstrap import start

if __name__ == "__main__":
    start()
