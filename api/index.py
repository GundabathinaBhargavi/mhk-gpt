import sys
import os
from pathlib import Path

# Add backend directory to Python path for imports
backend_path = str(Path(__file__).parent.parent / "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.app.main import app

# Vercel requires "app" to be available in the module
# This index.py acts as the serverless entry point
