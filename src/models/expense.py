"""Expense models and request/response validation schemas."""

from datetime import date
from typing import Annotated
from pydantic import BaseModel, Field, field_validator


class ExpenseBase(BaseModel):
    """Base schema for expense data with domain validation rules."""

    title: Annotated[
        str,
        Field(
            description="Short title or summary of the expense.",
            examples=["Groceries at Supermarket"],
        ),
    ]
    amount: Annotated[
        float,
        Field(
            description="Expense amount in currency units. Must be strictly positive (> 0).",
            examples=[45.50],
        ),
    ]
    category: Annotated[
        str,
        Field(
            description="Category classifying the expense.",
            examples=["Food"],
        ),
    ]
    date: Annotated[
        date,
        Field(
            description="Date when expense occurred (YYYY-MM-DD). Cannot be in the future.",
            examples=["2026-08-01"],
        ),
    ]

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Validate title is non-empty and non-whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Expense title cannot be empty or whitespace only.")
        return stripped

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        """Validate category is non-empty and non-whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Expense category cannot be empty or whitespace only.")
        return stripped

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: float) -> float:
        """Validate amount is strictly greater than zero and rounded to 2 decimal places."""
        if value <= 0:
            raise ValueError("Expense amount must be strictly greater than zero.")
        return round(value, 2)

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: date) -> date:
        """Validate expense date is not in the future."""
        if value > date.today():
            raise ValueError("Expense date cannot be in the future.")
        return value


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Team Lunch",
                "amount": 85.50,
                "category": "Food",
                "date": "2026-08-01",
            }
        }
    }


class ExpenseResponse(ExpenseBase):
    """Schema representing a stored expense returned by the API."""

    id: Annotated[
        int,
        Field(
            description="Unique auto-incrementing integer identifier for the expense.",
            examples=[1],
        ),
    ]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Team Lunch",
                "amount": 85.50,
                "category": "Food",
                "date": "2026-08-01",
            }
        }
    }


class OverallTotalResponse(BaseModel):
    """Schema for total expense response across all categories."""

    total: Annotated[
        float,
        Field(
            description="Sum of all expenses rounded to 2 decimal places.",
            examples=[1250.75],
        ),
    ]


class CategoryTotalResponse(BaseModel):
    """Schema for total expense response filtered by category."""

    category: Annotated[
        str,
        Field(
            description="Expense category filter requested.",
            examples=["Food"],
        ),
    ]
    total: Annotated[
        float,
        Field(
            description="Sum of all expenses in specified category rounded to 2 decimal places.",
            examples=[350.25],
        ),
    ]
