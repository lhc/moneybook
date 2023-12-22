import datetime
import decimal

import pytest
from django.urls import reverse
from model_bakery import baker

from moneybook.bookkeeping.models import Transaction


@pytest.mark.django_db
def test_can_get_transactions_without_providing_year(client):
    response = client.get(reverse("bookkeeping:transactions"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_can_get_transactions_by_year(client):
    response = client.get(reverse("bookkeeping:year-transactions", args=(2023,)))

    assert response.status_code == 200


@pytest.mark.django_db
def test_exclude_transaction_of_different_year(client):
    transaction_2021 = baker.make(Transaction, date=datetime.date(2021, 4, 28))
    transaction_2022 = baker.make(Transaction, date=datetime.date(2022, 3, 2))
    transaction_2023 = baker.make(Transaction, date=datetime.date(2023, 12, 8))

    response = client.get(reverse("bookkeeping:year-transactions", args=(2022,)))

    transactions = response.context.get("transactions") or []
    assert len(transactions) == 1

    references = [transaction["reference"] for transaction in transactions]
    assert transaction_2021.reference not in references
    assert transaction_2022.reference in references
    assert transaction_2023.reference not in references


@pytest.mark.django_db
def test_year_transactions_should_have_initial_balance_from_previous_years(client):
    baker.make(
        Transaction, date=datetime.date(2021, 3, 2), amount=decimal.Decimal("50.0")
    )
    baker.make(
        Transaction, date=datetime.date(2021, 4, 2), amount=decimal.Decimal("60.0")
    )
    baker.make(
        Transaction, date=datetime.date(2022, 4, 2), amount=decimal.Decimal("600.0")
    )
    baker.make(
        Transaction, date=datetime.date(2023, 4, 2), amount=decimal.Decimal("7000.0")
    )

    response = client.get(reverse("bookkeeping:year-transactions", args=(2022,)))

    assert "initial_balance" in response.context
    assert response.context["initial_balance"] == decimal.Decimal("110.0")


@pytest.mark.django_db
def test_no_balance_from_previous_year(client):
    baker.make(
        Transaction, date=datetime.date(2021, 3, 2), amount=decimal.Decimal("50.0")
    )

    response = client.get(reverse("bookkeeping:year-transactions", args=(2021,)))

    assert "initial_balance" in response.context
    assert response.context["initial_balance"] == decimal.Decimal("0.0")


@pytest.mark.django_db
def test_no_balance_at_all(client):
    response = client.get(reverse("bookkeeping:transactions"))

    assert "initial_balance" in response.context
    assert response.context["initial_balance"] == decimal.Decimal("0.0")
