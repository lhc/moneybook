import datetime
import decimal

import pytest
from model_bakery import baker

from thebook.bookkeeping.models import Transaction


@pytest.fixture
def summary_transactions():
    baker.make(
        Transaction,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2023, 2, 1),
        amount=decimal.Decimal("1"),
    )
    baker.make(
        Transaction,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2023, 4, 1),
        amount=decimal.Decimal("3"),
    )
    baker.make(
        Transaction,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 4, 1),
        amount=decimal.Decimal("5"),
    )
    baker.make(
        Transaction,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 4, 1),
        amount=decimal.Decimal("7"),
    )
    baker.make(
        Transaction,
        transaction_type=Transaction.EXPENSE,
        date=datetime.date(2024, 4, 1),
        amount=decimal.Decimal("9"),
    )
    baker.make(
        Transaction,
        transaction_type=Transaction.EXPENSE,
        date=datetime.date(2024, 4, 13),
        amount=decimal.Decimal("13"),
    )
    baker.make(
        Transaction,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 3, 1),
        amount=decimal.Decimal("17"),
    )
