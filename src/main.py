"""FastAPI main application entry point."""

from fastapi import FastAPI
from src.routes.expenses import router as expense_router

app = FastAPI(
    title="Smart Expense Tracker API",
    description=(
        "A REST API for managing personal expenses, built with FastAPI, "
        "Pydantic v2, Pytest, and local JSON storage."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Expenses",
            "description": "Operations for managing personal expenses.",
        }
    ],
)

app.include_router(expense_router)
