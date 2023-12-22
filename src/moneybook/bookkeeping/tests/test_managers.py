import datetime
import decimal

import pytest
from model_bakery import baker

from moneybook.bookkeeping.models import Transaction


@pytest.fixture
def transactions():
    baker.make(
        Transaction, date=datetime.date(2021, 1, 1), amount=decimal.Decimal("10.1")
    )
    baker.make(
        Transaction, date=datetime.date(2021, 2, 2), amount=decimal.Decimal("20.1")
    )
    baker.make(
        Transaction, date=datetime.date(2022, 3, 3), amount=decimal.Decimal("300.1")
    )
    baker.make(
        Transaction, date=datetime.date(2022, 4, 4), amount=decimal.Decimal("400.1")
    )
    baker.make(
        Transaction, date=datetime.date(2023, 5, 5), amount=decimal.Decimal("5000.1")
    )
    baker.make(
        Transaction, date=datetime.date(2023, 6, 6), amount=decimal.Decimal("6000.1")
    )


@pytest.mark.django_db
def test_get_transactions_by_specific_year():
    transaction_2021 = baker.make(Transaction, date=datetime.date(2021, 4, 28))
    transaction_2022 = baker.make(Transaction, date=datetime.date(2022, 3, 2))
    transaction_2023 = baker.make(Transaction, date=datetime.date(2023, 12, 8))

    transactions = Transaction.objects.for_year(2022)

    assert len(transactions) == 1
    assert transaction_2021 not in transactions
    assert transaction_2022 in transactions
    assert transaction_2023 not in transactions


@pytest.mark.django_db
@pytest.mark.parametrize(
    "year,expected_initial_balance",
    [
        (2020, decimal.Decimal("0")),
        (2021, decimal.Decimal("0")),
        (2022, decimal.Decimal("30.2")),
        (2023, decimal.Decimal("730.4")),
        (2024, decimal.Decimal("11730.6")),
    ],
)
def test_get_initial_balance_for_year(transactions, year, expected_initial_balance):
    initial_balance = Transaction.objects.initial_balance_for_year(year)

    assert initial_balance == expected_initial_balance
