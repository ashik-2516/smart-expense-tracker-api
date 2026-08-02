"""Integration tests for REST API endpoints using FastAPI TestClient."""

from datetime import date, timedelta
from fastapi.testclient import TestClient


def test_create_expense_success(client: TestClient) -> None:
    """Test POST /expenses creates an expense with HTTP 201."""
    payload = {
        "title": "Grocery Shopping",
        "amount": 54.20,
        "category": "Food",
        "date": "2026-08-01",
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Grocery Shopping"
    assert data["amount"] == 54.20
    assert data["category"] == "Food"
    assert data["date"] == "2026-08-01"


def test_create_expense_validation_failures(client: TestClient) -> None:
    """Test POST /expenses rejects invalid payloads with HTTP 422."""
    valid_base = {
        "title": "Valid Title",
        "amount": 10.0,
        "category": "Valid Category",
        "date": "2026-08-01",
    }

    # Missing fields
    res = client.post("/expenses", json={"title": "Missing rest"})
    assert res.status_code == 422

    # Empty title
    payload = {**valid_base, "title": ""}
    assert client.post("/expenses", json=payload).status_code == 422

    # Whitespace title
    payload = {**valid_base, "title": "   "}
    assert client.post("/expenses", json=payload).status_code == 422

    # Empty category
    payload = {**valid_base, "category": ""}
    assert client.post("/expenses", json=payload).status_code == 422

    # Zero amount
    payload = {**valid_base, "amount": 0.0}
    assert client.post("/expenses", json=payload).status_code == 422

    # Negative amount
    payload = {**valid_base, "amount": -25.0}
    assert client.post("/expenses", json=payload).status_code == 422

    # Invalid date format
    payload = {**valid_base, "date": "2026/08/01"}
    assert client.post("/expenses", json=payload).status_code == 422

    # Future date
    future_date = (date.today() + timedelta(days=5)).isoformat()
    payload = {**valid_base, "date": future_date}
    assert client.post("/expenses", json=payload).status_code == 422


def test_create_expense_invalid_json(client: TestClient) -> None:
    """Test POST /expenses rejects malformed JSON body."""
    response = client.post(
        "/expenses",
        content="{title: invalid_json}",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_get_all_expenses_and_filtering(client: TestClient) -> None:
    """Test GET /expenses and GET /expenses?category=."""
    client.post("/expenses", json={"title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Taxi", "amount": 22.0, "category": "Travel", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Lunch", "amount": 15.0, "category": "food", "date": "2026-08-01"})

    all_res = client.get("/expenses")
    assert all_res.status_code == 200
    assert len(all_res.json()) == 3

    filter_res = client.get("/expenses?category=FOOD")
    assert filter_res.status_code == 200
    filtered_data = filter_res.json()
    assert len(filtered_data) == 2
    assert {item["title"] for item in filtered_data} == {"Coffee", "Lunch"}


def test_get_total_expenses_overall(client: TestClient) -> None:
    """Test GET /expenses/total returns overall sum."""
    client.post("/expenses", json={"title": "Item A", "amount": 100.0, "category": "CatA", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Item B", "amount": 50.5, "category": "CatB", "date": "2026-08-01"})

    res = client.get("/expenses/total")
    assert res.status_code == 200
    assert res.json() == {"total": 150.5}


def test_get_total_expenses_by_category(client: TestClient) -> None:
    """Test GET /expenses/total?category= returns sum for specific category."""
    client.post("/expenses", json={"title": "Flight", "amount": 400.0, "category": "Travel", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Hotel", "amount": 250.0, "category": "travel", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Dinner", "amount": 60.0, "category": "Food", "date": "2026-08-01"})

    res = client.get("/expenses/total?category=TRAVEL")
    assert res.status_code == 200
    assert res.json() == {"category": "TRAVEL", "total": 650.0}


def test_delete_expense_success_204(client: TestClient) -> None:
    """Test DELETE /expenses/{id} returns 204 No Content."""
    create_res = client.post(
        "/expenses",
        json={"title": "To Delete", "amount": 10.0, "category": "Misc", "date": "2026-08-01"},
    )
    expense_id = create_res.json()["id"]

    delete_res = client.delete(f"/expenses/{expense_id}")
    assert delete_res.status_code == 204
    assert delete_res.content == b""

    list_res = client.get("/expenses")
    assert len(list_res.json()) == 0


def test_delete_expense_not_found_404(client: TestClient) -> None:
    """Test DELETE /expenses/{id} returns 404 for non-existent ID."""
    res = client.delete("/expenses/9999")
    assert res.status_code == 404
    assert res.json()["detail"] == "Expense with ID 9999 not found."


def test_delete_expense_invalid_id_type_422(client: TestClient) -> None:
    """Test DELETE /expenses/{id} returns 422 for non-integer ID."""
    res = client.delete("/expenses/abc")
    assert res.status_code == 422
