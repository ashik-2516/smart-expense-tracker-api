# Smart Expense Tracker API

A lightweight REST API for managing personal expenses, built with Python 3.12, FastAPI, Pydantic v2, and local JSON storage.

Created by **S. Ashik** as part of the Software Engineering Apprenticeship take-home assignment.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Design Decisions](#design-decisions)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)
- [Example Request](#example-request)
- [Assumptions](#assumptions)
- [Future Improvements](#future-improvements)

---

## Overview

The Smart Expense Tracker API allows users to create, retrieve, filter, summarize, and delete personal expense records. Data is stored locally in a JSON file, with validation handled through Pydantic and interactive API documentation provided through FastAPI's OpenAPI/Swagger interface.

---

## Features

- Create a new expense
- View all expenses
- Filter expenses by category (case-insensitive)
- Calculate total expenses (overall and by category)
- Delete an expense by integer ID
- Input validation (non-empty titles/categories, positive amounts, valid/non-future dates)
- Local JSON persistence with atomic writes
- Interactive Swagger / OpenAPI documentation (`/docs`)

---

## Design Decisions

- **JSON Storage**: Chosen because the assignment permits local file persistence without requiring an external database.
- **Layered Architecture**: Business logic is separated from API routes to improve maintainability and testability.
- **Atomic File Writes**: Temporary files and atomic replacement are used to reduce the risk of data corruption during write operations.
- **OpenAPI / Swagger**: Implemented as the single bonus feature to provide interactive API documentation and endpoint testing.

---

## Project Structure

```text
.
├── README.md                  # Setup, usage, API documentation, and design notes
├── AI_NOTES.md                 # Report on AI usage, evaluations, and decisions
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore rules (includes expenses.json)
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── expense.py          # Pydantic v2 domain schemas and validators
│   ├── storage/
│   │   ├── __init__.py
│   │   └── json_storage.py     # Resilient JSON file storage engine
│   ├── services/
│   │   ├── __init__.py
│   │   └── expense_service.py  # Business logic service layer
│   └── routes/
│       ├── __init__.py
│       └── expenses.py         # REST API routes
└── tests/
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures and temporary storage setup
    ├── test_models.py          # Validation unit tests
    ├── test_storage.py         # Storage resilience unit tests
    ├── test_services.py        # Business logic unit tests
    └── test_api.py             # REST API integration tests
```

---

## Installation

Create and activate a virtual environment (recommended).

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## Running the API

Start the development server:

```bash
python -m uvicorn src.main:app --reload
```

Once the server is running:

- API Base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI Schema: `http://127.0.0.1:8000/openapi.json`

---

## Running Tests

Execute the complete test suite:

```bash
python -m pytest -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Create a new expense |
| GET | `/expenses` | Retrieve all expenses |
| GET | `/expenses?category=Food` | Filter expenses by category |
| GET | `/expenses/total` | Get overall expense total |
| GET | `/expenses/total?category=Food` | Get category-wise total |
| DELETE | `/expenses/{id}` | Delete an expense |

---

## Example Request

### Create an Expense

POST `/expenses`

```json
{
  "title": "Groceries",
  "amount": 450.75,
  "category": "Food",
  "date": "2026-08-02"
}
```

### Response

```json
{
  "id": 1,
  "title": "Groceries",
  "amount": 450.75,
  "category": "Food",
  "date": "2026-08-02"
}
```

---

## Assumptions

- Expenses are stored in a local `expenses.json` file.
- Expense IDs are assigned sequentially.
- Category filtering is case-insensitive.
- Dates cannot be in the future.
- The application is designed for a single-user, local environment.

---

## Future Improvements

- Replace JSON storage with a database.
- Add update (`PUT`) endpoint.
- Add pagination and sorting.
- Add authentication and user accounts.

---

This project was intentionally designed to be simple, maintainable, and aligned with the assignment requirements while demonstrating clean architecture, validation, testing, and REST API best practices.
