"""Unit tests for JSON storage resilience, atomic writes, and corruption handling."""

import os
import pytest
from fastapi import HTTPException
from src.storage.json_storage import JSONStorage


def test_storage_auto_creates_missing_file(temp_json_file: str) -> None:
    """Test that JSONStorage automatically creates the JSON file if missing."""
    assert not os.path.exists(temp_json_file)
    storage = JSONStorage(file_path=temp_json_file)
    assert os.path.exists(temp_json_file)
    assert storage.load_all() == []


def test_storage_handles_empty_file(temp_json_file: str) -> None:
    """Test recovery from an empty (0-byte) storage file."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("")

    storage = JSONStorage(file_path=temp_json_file)
    assert storage.load_all() == []


def test_storage_handles_whitespace_only_file(temp_json_file: str) -> None:
    """Test recovery from a whitespace-only storage file."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("   \n  \t ")

    storage = JSONStorage(file_path=temp_json_file)
    assert storage.load_all() == []


def test_storage_raises_500_on_corrupt_json(temp_json_file: str) -> None:
    """Test 500 error handling when storage file contains malformed JSON."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("{invalid_json: true, missing_quotes}")

    storage = JSONStorage(file_path=temp_json_file)
    with pytest.raises(HTTPException) as exc:
        storage.load_all()
    assert exc.value.status_code == 500
    assert "invalid JSON" in exc.value.detail


def test_storage_resets_on_non_list_json(temp_json_file: str) -> None:
    """Test that a JSON object (dict instead of list) is handled safely by returning an empty list."""
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write('{"key": "value"}')

    storage = JSONStorage(file_path=temp_json_file)
    assert storage.load_all() == []


def test_atomic_save_and_reload(temp_json_file: str) -> None:
    """Test saving records atomically and re-reading them."""
    storage = JSONStorage(file_path=temp_json_file)
    sample_data = [
        {
            "id": 1,
            "title": "Dinner",
            "amount": 35.0,
            "category": "Food",
            "date": "2026-08-01",
        }
    ]
    storage.save_all(sample_data)
    loaded = storage.load_all()
    assert loaded == sample_data
    assert not os.path.exists(f"{temp_json_file}.tmp")
