"""Pytest configuration and shared test fixtures."""

from typing import Generator
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.routes.expenses import get_expense_service
from src.services.expense_service import ExpenseService
from src.storage.json_storage import JSONStorage


@pytest.fixture
def temp_json_file(tmp_path) -> str:
    """Fixture providing an isolated temporary JSON file path."""
    file_path = tmp_path / "test_expenses.json"
    return str(file_path)


@pytest.fixture
def test_storage(temp_json_file: str) -> JSONStorage:
    """Fixture providing a JSONStorage instance tied to temporary storage."""
    return JSONStorage(file_path=temp_json_file)


@pytest.fixture
def test_service(test_storage: JSONStorage) -> ExpenseService:
    """Fixture providing an ExpenseService instance using test storage."""
    return ExpenseService(storage=test_storage)


@pytest.fixture
def client(test_storage: JSONStorage) -> Generator[TestClient, None, None]:
    """Fixture providing a FastAPI TestClient with storage dependency override."""
    test_svc = ExpenseService(storage=test_storage)

    def override_get_service() -> ExpenseService:
        return test_svc

    app.dependency_overrides[get_expense_service] = override_get_service
    yield TestClient(app)
    app.dependency_overrides.clear()
