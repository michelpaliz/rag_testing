This file is your **agenda preprocessor**. It reads raw, unstructured text from your `agenda.txt` file and converts each line into a structured Python dictionary containing key metadata. Here's what each part does:

---

### 🔹 Imports

```python
from utils.static.paths import AGENDA_FILE
import re, time
from pathlib import Path
from datetime import datetime
from typing import List, Dict
```

* **`AGENDA_FILE`**: Static path to your `agenda.txt`, centralized in one config file.
* **`re`** and **`datetime`**: Used to extract and format dates.
* **`Path`**: For reading the file in a clean, cross-platform way.
* **Typing**: Indicates the function returns `List[Dict]` for clarity and IDE support.

---

### 🔹 `parse_line(line: str) -> Dict`

This function processes one line of the agenda and extracts structure:

```python
tags = []
low = line.lower()
```

#### 1. **Tag detection**:

Adds `"urgente"`, `"pendiente"`, or `"llamar"` if found in the line.

#### 2. **Date extraction**:

```python
re.search(r"(\d{2}/\d{2}/\d{2})", line)
```

* Looks for patterns like `27/05/25` and converts them to ISO: `2025-05-27`.
* Also removes the date from the line for cleaner text output.

#### 3. **Return structured dictionary**:

```python
{
    "texto": line.strip("• ").strip(),
    "etiquetas": tags,
    "fecha": date,
    "categoria": None
}
```

---

### 🔹 `preprocess_agenda(path: str = str(AGENDA_FILE)) -> List[Dict]`

* Reads the full agenda file.
* Splits it into lines.
* Passes each line to `parse_line()`.
* Returns a **list of structured dictionaries** (tasks).

Example output:

```python
{
  "texto": "Llamar a gestoría para resolver incidencia",
  "etiquetas": ["llamar"],
  "fecha": "2025-05-23",
  "categoria": None
}
```

---

### 🔹 `if __name__ == "__main__":`

This block runs if the script is executed directly. It:

* Calls `preprocess_agenda()`
* Prints the first 5 structured items for a quick preview

---

### ✅ Why it's important

This file:

* Converts unstructured text into structured, filterable data
* Prepares your agenda items for **embedding and RAG retrieval**
* Can also be reused for export (e.g. to JSON or CSV)

Let me know if you want to add more tag rules or handle more date formats!
