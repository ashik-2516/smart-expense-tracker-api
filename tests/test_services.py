"""Unit tests for ExpenseService business logic, auto-increment IDs, and filtering."""

from datetime import date
import pytest
from fastapi import HTTPException

from src.models.expense import ExpenseCreate
from src.services.expense_service import ExpenseService


def test_auto_incrementing_integer_ids(test_service: ExpenseService) -> None:
    """Test that created expenses receive sequential integer IDs starting from 1."""
    item1 = test_service.create_expense(
        ExpenseCreate(title="Coffee", amount=4.50, category="Food", date="2026-08-01")
    )
    item2 = test_service.create_expense(
        ExpenseCreate(title="Lunch", amount=15.00, category="Food", date="2026-08-01")
    )
    item3 = test_service.create_expense(
        ExpenseCreate(title="Bus Pass", amount=25.00, category="Transport", date="2026-08-01")
    )

    assert item1.id == 1
    assert item2.id == 2
    assert item3.id == 3


def test_case_insensitive_category_filtering(test_service: ExpenseService) -> None:
    """Test case-insensitive category filtering in get_all_expenses."""
    test_service.create_expense(
        ExpenseCreate(title="Pizza", amount=20.0, category="Food", date="2026-08-01")
    )
    test_service.create_expense(
        ExpenseCreate(title="Burger", amount=12.0, category="FOOD", date="2026-08-01")
    )
    test_service.create_expense(
        ExpenseCreate(title="Movie", amount=15.0, category="Entertainment", date="2026-08-01")
    )

    food_items = test_service.get_all_expenses(category="food")
    assert len(food_items) == 2
    assert {item.title for item in food_items} == {"Pizza", "Burger"}

    upper_food_items = test_service.get_all_expenses(category="FOOD")
    assert len(upper_food_items) == 2


def test_get_total_expenses_overall(test_service: ExpenseService) -> None:
    """Test overall total expense calculation."""
    test_service.create_expense(
        ExpenseCreate(title="Item A", amount=10.50, category="CatA", date="2026-08-01")
    )
    test_service.create_expense(
        ExpenseCreate(title="Item B", amount=20.25, category="CatB", date="2026-08-01")
    )

    total_resp = test_service.get_total_expenses()
    assert total_resp.total == 30.75


def test_get_total_expenses_by_category_case_insensitive(test_service: ExpenseService) -> None:
    """Test category total calculation with case-insensitivity."""
    test_service.create_expense(
        ExpenseCreate(title="Item 1", amount=10.0, category="Work", date="2026-08-01")
    )
    test_service.create_expense(
        ExpenseCreate(title="Item 2", amount=15.5, category="work", date="2026-08-01")
    )
    test_service.create_expense(
        ExpenseCreate(title="Item 3", amount=100.0, category="Personal", date="2026-08-01")
    )

    cat_total = test_service.get_total_expenses(category="WORK")
    assert cat_total.category == "WORK"
    assert cat_total.total == 25.50


def test_get_total_for_non_existent_category(test_service: ExpenseService) -> None:
    """Test that requesting total for a non-existent category returns 0.0."""
    cat_total = test_service.get_total_expenses(category="NonExistent")
    assert cat_total.category == "NonExistent"
    assert cat_total.total == 0.0


def test_delete_expense_success(test_service: ExpenseService) -> None:
    """Test deleting an expense by ID."""
    e1 = test_service.create_expense(
        ExpenseCreate(title="Item 1", amount=10.0, category="Cat", date="2026-08-01")
    )
    e2 = test_service.create_expense(
        ExpenseCreate(title="Item 2", amount=20.0, category="Cat", date="2026-08-01")
    )

    test_service.delete_expense(e1.id)
    remaining = test_service.get_all_expenses()
    assert len(remaining) == 1
    assert remaining[0].id == e2.id


def test_delete_last_expense_leaves_empty_list(test_service: ExpenseService) -> None:
    """Test that deleting the last expense results in an empty expense list."""
    e = test_service.create_expense(
        ExpenseCreate(title="Sole Item", amount=50.0, category="Misc", date="2026-08-01")
    )
    test_service.delete_expense(e.id)
    assert test_service.get_all_expenses() == []


def test_delete_non_existent_expense_raises_404(test_service: ExpenseService) -> None:
    """Test that attempting to delete a non-existent ID raises a 404 HTTPException."""
    with pytest.raises(HTTPException) as exc:
        test_service.delete_expense(999)
    assert exc.value.status_code == 404
    assert "999" in exc.value.detail
