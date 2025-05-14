import json
from pathlib import Path
from typing import Any


def load_json_data(path: Path) -> dict[str, Any]:
    """Load and parse a JSON file into a dictionary."""
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
