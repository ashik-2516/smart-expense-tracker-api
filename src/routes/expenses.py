"""API routes for expense management endpoints."""

from typing import List, Optional, Union
from fastapi import APIRouter, Depends, Query, Response, status

from src.models.expense import (
    CategoryTotalResponse,
    ExpenseCreate,
    ExpenseResponse,
    OverallTotalResponse,
)
from src.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_expense_service() -> ExpenseService:
    """Dependency provider for ExpenseService."""
    return ExpenseService()


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description="Creates a new expense record with auto-incrementing integer ID.",
)
def create_expense(
    expense_in: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    """Create a new expense item."""
    return service.create_expense(expense_in)


@router.get(
    "",
    response_model=List[ExpenseResponse],
    status_code=status.HTTP_200_OK,
    summary="List all expenses",
    description="Retrieves all expenses, optionally filtered by category (case-insensitive).",
)
def list_expenses(
    category: Optional[str] = Query(
        None,
        description="Optional category to filter expenses (case-insensitive).",
        examples=["Food"],
    ),
    service: ExpenseService = Depends(get_expense_service),
) -> List[ExpenseResponse]:
    """Retrieve expense records."""
    return service.get_all_expenses(category=category)


@router.get(
    "/total",
    response_model=Union[CategoryTotalResponse, OverallTotalResponse],
    status_code=status.HTTP_200_OK,
    summary="Calculate total expenses",
    description="Calculates total expenses overall or for a specific category (case-insensitive).",
)
def get_total_expenses(
    category: Optional[str] = Query(
        None,
        description="Optional category to sum expenses for (case-insensitive).",
        examples=["Food"],
    ),
    service: ExpenseService = Depends(get_expense_service),
) -> Union[CategoryTotalResponse, OverallTotalResponse]:
    """Calculate expense totals."""
    return service.get_total_expenses(category=category)


@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense by ID",
    description="Deletes an expense record matching the specified integer ID.",
    responses={
        204: {"description": "Expense successfully deleted"},
        404: {"description": "Expense ID not found"},
    },
)
def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
) -> Response:
    """Delete an expense item by integer ID."""
    service.delete_expense(expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
