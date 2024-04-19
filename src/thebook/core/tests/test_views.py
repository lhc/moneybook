from django.urls import reverse


def test_dashboard_access(db, client):
    response = client.get(reverse("core:dashboard"))

    assert response.status_code == 200


def test_dashboard_expected_context(db, client):
    response = client.get(reverse("core:dashboard"))

    assert "transactions_summary" in response.context
    assert "cash_books_summary" in response.context
