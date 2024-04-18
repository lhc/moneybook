import datetime
import decimal

import pytest
from model_bakery import baker

from thebook.bookkeeping.models import CashBook, Transaction


@pytest.fixture
def cash_book_with_transactions():
    cash_book = baker.make(CashBook, name="Test Cash Book")

    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.DEPOSIT,
        date=datetime.date(2024, 3, 1),
        amount=decimal.Decimal("200"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 3, 5),
        amount=decimal.Decimal("38.9"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 3, 10),
        amount=decimal.Decimal("78.42"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.EXPENSE,
        date=datetime.date(2024, 3, 5),
        amount=decimal.Decimal("18.9"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.EXPENSE,
        date=datetime.date(2024, 3, 10),
        amount=decimal.Decimal("28.42"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.WITHDRAW,
        date=datetime.date(2024, 3, 25),
        amount=decimal.Decimal("150"),
    )

    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.DEPOSIT,
        date=datetime.date(2024, 4, 1),
        amount=decimal.Decimal("170"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 4, 5),
        amount=decimal.Decimal("50.78"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.INCOME,
        date=datetime.date(2024, 4, 10),
        amount=decimal.Decimal("13.26"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.EXPENSE,
        date=datetime.date(2024, 4, 5),
        amount=decimal.Decimal("6.42"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.EXPENSE,
        date=datetime.date(2024, 4, 10),
        amount=decimal.Decimal("73.23"),
    )
    baker.make(
        Transaction,
        cash_book=cash_book,
        transaction_type=Transaction.WITHDRAW,
        date=datetime.date(2024, 4, 12),
        amount=decimal.Decimal("80"),
    )

    return cash_book
