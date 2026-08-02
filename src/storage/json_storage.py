"""JSON file storage implementation with atomic writes and corruption recovery."""

import json
import os
from typing import Any, Dict, List
from fastapi import HTTPException


class JSONStorage:
    """Handles persistent storage of expense records in a local JSON file."""

    def __init__(self, file_path: str = "expenses.json") -> None:
        """Initialize storage with a target file path."""
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create the storage file if it does not exist."""
        if not os.path.exists(self.file_path):
            self.save_all([])

    def load_all(self) -> List[Dict[str, Any]]:
        """Load and return all expense records from the JSON storage file."""
        if not os.path.exists(self.file_path):
            self._ensure_file_exists()
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                    return []
                return data
        except json.JSONDecodeError as err:
            raise HTTPException(
                status_code=500,
                detail=f"Storage file '{self.file_path}' contains invalid JSON.",
            ) from err
        except OSError as err:
            raise HTTPException(
                status_code=500,
                detail="Unable to read storage file due to file system error.",
            ) from err

    def save_all(self, expenses: List[Dict[str, Any]]) -> None:
        """Atomically write expense records to disk using a temporary file."""
        tmp_file_path = f"{self.file_path}.tmp"
        try:
            dirname = os.path.dirname(self.file_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            with open(tmp_file_path, "w", encoding="utf-8") as tmp_file:
                json.dump(expenses, tmp_file, indent=2, ensure_ascii=False)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            os.replace(tmp_file_path, self.file_path)
        except OSError as err:
            if os.path.exists(tmp_file_path):
                try:
                    os.remove(tmp_file_path)
                except OSError:
                    pass
            raise HTTPException(
                status_code=500,
                detail="Failed to persist expense data to disk.",
            ) from err
