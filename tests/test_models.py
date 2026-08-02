"""Unit tests for Pydantic v2 domain models and validators."""

from datetime import date, timedelta
import pytest
from pydantic import ValidationError

from src.models.expense import (
    CategoryTotalResponse,
    ExpenseCreate,
    ExpenseResponse,
    OverallTotalResponse,
)


def test_valid_expense_create() -> None:
    """Test creating a valid expense payload."""
    data = {
        "title": "Groceries",
        "amount": 45.99,
        "category": "Food",
        "date": "2026-08-01",
    }
    expense = ExpenseCreate(**data)
    assert expense.title == "Groceries"
    assert expense.amount == 45.99
    assert expense.category == "Food"
    assert expense.date == date(2026, 8, 1)


def test_empty_and_whitespace_title_validation() -> None:
    """Test that empty or whitespace-only titles are rejected."""
    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="", amount=10.0, category="Food", date="2026-08-01")
    assert "Expense title cannot be empty" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="   ", amount=10.0, category="Food", date="2026-08-01")
    assert "Expense title cannot be empty" in str(exc.value)


def test_empty_and_whitespace_category_validation() -> None:
    """Test that empty or whitespace-only categories are rejected."""
    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="Lunch", amount=10.0, category="", date="2026-08-01")
    assert "Expense category cannot be empty" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="Lunch", amount=10.0, category="   ", date="2026-08-01")
    assert "Expense category cannot be empty" in str(exc.value)


def test_zero_and_negative_amount_validation() -> None:
    """Test that zero or negative amounts are rejected."""
    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="Coffee", amount=0.0, category="Food", date="2026-08-01")
    assert "must be strictly greater than zero" in str(exc.value)

    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="Coffee", amount=-15.50, category="Food", date="2026-08-01")
    assert "must be strictly greater than zero" in str(exc.value)


def test_future_date_validation() -> None:
    """Test that future dates are rejected."""
    future_date = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(ValidationError) as exc:
        ExpenseCreate(title="Ticket", amount=50.0, category="Travel", date=future_date)
    assert "Expense date cannot be in the future" in str(exc.value)


def test_title_and_category_whitespace_trimming() -> None:
    """Test that leading/trailing whitespace is automatically trimmed."""
    expense = ExpenseCreate(
        title="  Book purchase  ",
        amount=19.99,
        category="  Education  ",
        date="2026-08-01",
    )
    assert expense.title == "Book purchase"
    assert expense.category == "Education"


def test_amount_rounding_to_two_decimals() -> None:
    """Test that amounts with excess precision are rounded to two decimal places."""
    expense = ExpenseCreate(
        title="Taxi",
        amount=14.556,
        category="Transport",
        date="2026-08-01",
    )
    assert expense.amount == 14.56


def test_unicode_title_and_category() -> None:
    """Test support for Unicode characters in title and category."""
    expense = ExpenseCreate(
        title="Café ☕ & Croissant 🥐",
        amount=12.50,
        category="Alimentação 🍱",
        date="2026-08-01",
    )
    assert expense.title == "Café ☕ & Croissant 🥐"
    assert expense.category == "Alimentação 🍱"


def test_expense_response_model() -> None:
    """Test ExpenseResponse schema instantiation."""
    resp = ExpenseResponse(
        id=1,
        title="Laptop",
        amount=1200.00,
        category="Tech",
        date=date(2026, 8, 1),
    )
    assert resp.id == 1
    assert resp.title == "Laptop"


def test_totals_response_models() -> None:
    """Test overall and category total response schemas."""
    overall = OverallTotalResponse(total=250.75)
    assert overall.total == 250.75

    cat_total = CategoryTotalResponse(category="Food", total=100.50)
    assert cat_total.category == "Food"
    assert cat_total.total == 100.50
