# utils/static/paths.py
from pathlib import Path

# ──> project folder is two levels up from this file (utils/static/paths.py)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# raw data
DATA_DIR = PROJECT_ROOT / "data"
AGENDA_FILE = DATA_DIR / "agenda.txt"

# where your single, shared Chroma DB lives
VECTORSTORE_DIR = PROJECT_ROOT / "chroma_db"
