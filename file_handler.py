import json
import os
from typing import Any, List, Dict


def load_json(filepath: str, default: Any = None) -> Any:
    """
    Safely load data from a JSON file.
    Handles missing files, corrupt data, and empty files.
    """
    if default is None:
        default = []

    # If file doesn't exist, create parent directory and initialize empty default
    if not os.path.exists(filepath):
        parent_dir = os.path.dirname(filepath)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        save_json(filepath, default)
        return default

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                # File is empty
                return default
            return json.loads(content)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to read {filepath} ({e}). Returning default fallback.")
        return default


def save_json(filepath: str, data: Any) -> bool:
    """
    Save data to a JSON file safely with indentation.
    Ensures directory exists before writing.
    """
    try:
        parent_dir = os.path.dirname(filepath)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError as e:
        print(f"Error saving data to {filepath}: {e}")
        return False
