"""Expense business logic service layer."""

from typing import List, Optional, Union
from fastapi import HTTPException

from src.models.expense import (
    CategoryTotalResponse,
    ExpenseCreate,
    ExpenseResponse,
    OverallTotalResponse,
)
from src.storage.json_storage import JSONStorage


class ExpenseService:
    """Business logic coordinator for expense operations."""

    def __init__(self, storage: Optional[JSONStorage] = None) -> None:
        """Initialize service with storage dependency injection."""
        self.storage = storage or JSONStorage()

    def _generate_next_id(self, expenses: List[dict]) -> int:
        """Generate next sequential integer ID."""
        if not expenses:
            return 1
        existing_ids = [item.get("id", 0) for item in expenses if isinstance(item.get("id"), int)]
        return max(existing_ids, default=0) + 1

    def create_expense(self, expense_in: ExpenseCreate) -> ExpenseResponse:
        """Create and persist a new expense record."""
        expenses = self.storage.load_all()
        new_id = self._generate_next_id(expenses)

        record = {
            "id": new_id,
            "title": expense_in.title,
            "amount": expense_in.amount,
            "category": expense_in.category,
            "date": expense_in.date.isoformat(),
        }

        expenses.append(record)
        self.storage.save_all(expenses)
        return ExpenseResponse(**record)

    def get_all_expenses(self, category: Optional[str] = None) -> List[ExpenseResponse]:
        """Retrieve all expenses, optionally filtered by category (case-insensitive)."""
        raw_records = self.storage.load_all()

        if category is not None:
            clean_category = category.strip().lower()
            raw_records = [
                rec for rec in raw_records
                if rec.get("category", "").strip().lower() == clean_category
            ]

        return [ExpenseResponse(**rec) for rec in raw_records]

    def get_total_expenses(
        self, category: Optional[str] = None
    ) -> Union[OverallTotalResponse, CategoryTotalResponse]:
        """Calculate total amount spent overall or for a specific category."""
        raw_records = self.storage.load_all()

        if category is not None:
            clean_category = category.strip().lower()
            matching_records = [
                rec for rec in raw_records
                if rec.get("category", "").strip().lower() == clean_category
            ]
            total_amount = sum(rec.get("amount", 0.0) for rec in matching_records)
            return CategoryTotalResponse(
                category=category.strip(),
                total=round(total_amount, 2),
            )

        total_amount = sum(rec.get("amount", 0.0) for rec in raw_records)
        return OverallTotalResponse(total=round(total_amount, 2))

    def delete_expense(self, expense_id: int) -> None:
        """Delete an expense record by its integer ID."""
        raw_records = self.storage.load_all()
        initial_length = len(raw_records)

        updated_records = [rec for rec in raw_records if rec.get("id") != expense_id]

        if len(updated_records) == initial_length:
            raise HTTPException(
                status_code=404,
                detail=f"Expense with ID {expense_id} not found.",
            )

        self.storage.save_all(updated_records)
