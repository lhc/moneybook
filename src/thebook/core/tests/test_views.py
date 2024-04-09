import decimal

import pytest
from django.urls import reverse


def test_dashboard_access(db, client):
    response = client.get(reverse("core:dashboard"))

    assert response.status_code == 200


def test_dashboard_expected_context(db, client):
    response = client.get(reverse("core:dashboard"))

    assert response.context.get("incomes__current_month") == decimal.Decimal("0")
    assert response.context.get("expenses__current_month") == decimal.Decimal("0")
    assert response.context.get("balance__current_month") == decimal.Decimal("0")
    assert response.context.get("balance__current_year") == decimal.Decimal("0")


@pytest.mark.freeze_time("2024-04-08")
def test_dashboard_has_transactions_summary_in_context(
    db, client, summary_transactions
):
    response = client.get(reverse("core:dashboard"))

    assert response.context["incomes__current_month"] == decimal.Decimal("12")
    assert response.context["expenses__current_month"] == decimal.Decimal("22")
    assert response.context["balance__current_month"] == decimal.Decimal("-10")
    assert response.context["balance__current_year"] == decimal.Decimal("7")
