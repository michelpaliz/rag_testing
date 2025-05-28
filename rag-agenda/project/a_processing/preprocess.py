from utils.static.paths import AGENDA_FILE
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict


def parse_line(line: str) -> Dict:
    # Tags
    tags = []
    low = line.lower()
    if "urgente" in low:
        tags.append("urgente")
    if "pendiente" in low:
        tags.append("pendiente")
    if "llamar" in low:
        tags.append("llamar")

    # Date extraction (e.g., 27/05/25 → 2025-05-27)
    date_match = re.search(r"(\d{2}/\d{2}/\d{2})", line)
    date = None
    if date_match:
        try:
            date = datetime.strptime(date_match.group(1), "%d/%m/%y").date().isoformat()
        except ValueError:
            date = None
        # remove date token
        line = line.replace(date_match.group(1), "").replace(":", "").strip()

    return {
        "texto": line.strip("• ").strip(),
        "etiquetas": tags,
        "fecha": date,
        "categoria": None,  # Optional: use LLM later
    }


def preprocess_agenda(path: str = str(AGENDA_FILE)) -> List[Dict]:
    """
    Reads the agenda file and returns a list of structured items.
    Each item contains 'texto', 'etiquetas', 'fecha', 'categoria'.
    """
    raw_text = Path(path).read_text(encoding="utf-8")
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    return [parse_line(line) for line in lines]


if __name__ == "__main__":
    items = preprocess_agenda()
    for item in items[:5]:
        print(item)
