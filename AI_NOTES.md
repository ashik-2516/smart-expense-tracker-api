# AI Usage Report (AI_NOTES.md)

## Overview

AI tools were actively used throughout the development of the Smart Expense Tracker API. In accordance with the assignment guidelines, this document outlines how AI was utilized, which code components were generated versus human-written, how AI outputs were validated, and which AI suggestions were intentionally rejected.

---

## 1. Code Attribution: AI-Generated vs. Human-Written

### AI-Generated & Assisted Components
* **Boilerplate Code**: Initial structure for FastAPI endpoints (`src/routes/expenses.py`) and Pydantic schemas (`src/models/expense.py`).
* **OpenAPI Annotations**: OpenAPI tags, descriptions, and request/response schema examples for Swagger documentation.
* **Test Suite Foundation**: Base Pytest test cases for REST endpoints and schema validations.
* **Documentation Drafts**: Initial drafts for setup instructions and API reference tables.

### Human-Written, Refactored & Validated Components
* **Domain Validation Logic**: Enforced strict rules requiring `amount > 0`, non-empty/non-whitespace titles and categories, and rejecting future dates (`date > today`).
* **Resilient File Storage**: Implemented atomic writes using temporary files (`os.replace` and `os.fsync`) to guarantee data safety during crashes.
* **Auto-Increment Integer IDs**: Refined ID generation logic in `ExpenseService` to assign sequential integer IDs (`1, 2, 3...`).
* **Edge Case Testing & Debugging**: Expanded the test suite to verify 0-byte empty file recovery, malformed JSON detection, case-insensitive category filtering, and Unicode input support.

---

## 2. Validation & Code Changes

AI-generated outputs were thoroughly evaluated, tested, and modified before inclusion:

* **Pydantic Validation**: Updated AI-generated models to use Pydantic v2 `@field_validator` functions to handle whitespace trimming and strict date bounds.
* **Storage Reliability**: Modified the standard file writing snippet to flush and sync buffers to disk before replacing the target file atomically.
* **Test Isolation**: Created custom Pytest fixtures in `conftest.py` ensuring tests run against isolated temporary storage files (`tmp_path`) without mutating real data.

---

## 3. AI Suggestions Intentionally Not Adopted

1. **SQLite Database / SQLAlchemy ORM**:
   - **AI Suggestion**: Use SQLite with SQLAlchemy ORM and Alembic migrations.
   - **Reason for Rejection**: The assignment explicitly allowed local JSON storage and stated no database was required. Introducing an ORM would add unnecessary setup complexity.

2. **UUID String Identifiers**:
   - **AI Suggestion**: Generate UUID v4 strings for expense IDs.
   - **Reason for Rejection**: Sequential integer IDs (`1, 2, 3...`) are cleaner, simpler to read, and better aligned with the assignment prompt.

3. **Over-Engineered Exception Hierarchy & Config Files**:
   - **AI Suggestion**: Create custom exception classes (`StorageCorruptedError`, `ExpenseValidationError`) and a separate `config.py` module.
   - **Reason for Rejection**: Standard FastAPI `HTTPException` objects and direct Pydantic validation are simpler and avoid over-engineering.
