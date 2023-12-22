import datetime

import pytest
from django.urls import reverse
from model_bakery import baker

from moneybook.bookkeeping.models import Transaction
from moneybook.bookkeeping.views import transactions


def test_can_get_transactions_without_providing_year(rf, admin_user):
    request = rf.get(reverse("bookkeeping:transactions"))

    response = transactions(request)

    assert response.status_code == 200


def test_can_get_transactions_by_year(rf, admin_user):
    request = rf.get(reverse("bookkeeping:year-transactions", args=(2023,)))

    response = transactions(request, year=2023)

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
