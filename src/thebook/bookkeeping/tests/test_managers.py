import datetime
import decimal

import pytest
from model_bakery import baker

from thebook.bookkeeping.models import CashBook, Transaction


@pytest.fixture
def test_transactions():
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
def test_get_initial_balance_for_year(
    db, test_transactions, year, expected_initial_balance
):
    initial_balance = Transaction.objects.initial_balance_for_year(year)

    assert initial_balance == expected_initial_balance


def test_get_transaction_for_cash_book(db):
    cash_book_1 = baker.make(CashBook)
    cash_book_2 = baker.make(CashBook)  # noqa

    transaction_1 = baker.make(Transaction, cash_book=cash_book_1)
    transaction_2 = baker.make(Transaction, cash_book=cash_book_2)
    transaction_3 = baker.make(Transaction, cash_book=cash_book_1)

    transactions = Transaction.objects.for_cash_book(cash_book_2.slug)

    assert len(transactions) == 1
    assert transaction_1 not in transactions
    assert transaction_2 in transactions
    assert transaction_3 not in transactions


def test_get_transaction_for_cash_book_in_specific_year(db):
    cash_book_1 = baker.make(CashBook)
    cash_book_2 = baker.make(CashBook)  # noqa

    transaction_1 = baker.make(
        Transaction, date=datetime.date(2021, 4, 28), cash_book=cash_book_1
    )
    transaction_2 = baker.make(
        Transaction, date=datetime.date(2022, 3, 2), cash_book=cash_book_1
    )
    transaction_3 = baker.make(
        Transaction, date=datetime.date(2022, 3, 2), cash_book=cash_book_2
    )
    transaction_4 = baker.make(
        Transaction, date=datetime.date(2023, 12, 8), cash_book=cash_book_1
    )

    transactions = Transaction.objects.for_cash_book(cash_book_2.slug).for_year(2022)

    assert len(transactions) == 1
    assert transaction_1 not in transactions
    assert transaction_2 not in transactions
    assert transaction_3 in transactions
    assert transaction_4 not in transactions


def test_transactions_with_cumulative_sum(db):
    transaction_1 = baker.make(
        Transaction, date=datetime.date(2021, 4, 28), amount=decimal.Decimal("100.1")
    )
    transaction_2 = baker.make(
        Transaction, date=datetime.date(2022, 3, 2), amount=decimal.Decimal("142")
    )
    transaction_3 = baker.make(
        Transaction, date=datetime.date(2023, 3, 2), amount=decimal.Decimal("255.55")
    )

    transactions = Transaction.objects.with_cumulative_sum()
    assert len(transactions) == 3

    assert transactions[0].id == transaction_1.id
    assert transactions[0].cumulative_sum == transaction_1.amount

    assert transactions[1].id == transaction_2.id
    assert transactions[1].cumulative_sum == transaction_1.amount + transaction_2.amount

    assert transactions[2].id == transaction_3.id
    assert (
        transactions[2].cumulative_sum
        == transaction_1.amount + transaction_2.amount + transaction_3.amount
    )


def test_transactions_summary_with_transactions(db, cash_book_one_with_transactions):
    # Income and Expense of Cash Book different than the fixture
    extra_income = baker.make(  # noqa
        Transaction,
        date=datetime.date(2024, 4, 2),
        amount=decimal.Decimal("15"),
        transaction_type=Transaction.INCOME,
    )
    extra_expense = baker.make(  # noqa
        Transaction,
        date=datetime.date(2024, 4, 2),
        amount=decimal.Decimal("17.1"),
        transaction_type=Transaction.EXPENSE,
    )

    transactions_summary = Transaction.objects.summary(month=4, year=2024)

    assert transactions_summary["incomes_month"] == decimal.Decimal("79.04")
    assert transactions_summary["expenses_month"] == decimal.Decimal("96.75")
    assert transactions_summary["balance_month"] == decimal.Decimal("72.29")
    assert transactions_summary["balance_year"] == decimal.Decimal("192.29")
    assert transactions_summary["current_balance"] == decimal.Decimal("192.29")
    assert transactions_summary["month"] == 4
    assert transactions_summary["year"] == 2024


def test_cash_books_summary_with_transactions(
    db, cash_book_one_with_transactions, cash_book_two_with_transactions
):
    # Ordering by id to ensure that the first result is the Cash Book created in the fixture
    cash_books_summary = CashBook.objects.summary(month=4, year=2024).order_by("id")

    assert len(cash_books_summary) == 2

    first_summary = cash_books_summary[0]  # i.e. cash_book_one_with_transactions
    second_summary = cash_books_summary[1]  # i.e. cash_book_two_with_transactions

    assert first_summary.name == cash_book_one_with_transactions.name
    assert first_summary.slug == cash_book_one_with_transactions.slug
    assert first_summary.positive_balance_month == decimal.Decimal("234.04")
    assert first_summary.negative_balance_month == decimal.Decimal("159.65")
    assert first_summary.positive_current_balance == decimal.Decimal("551.36")
    assert first_summary.negative_current_balance == decimal.Decimal("356.97")
    assert first_summary.month == 4
    assert first_summary.year == 2024

    assert second_summary.name == cash_book_two_with_transactions.name
    assert second_summary.slug == cash_book_two_with_transactions.slug
    assert second_summary.positive_balance_month == decimal.Decimal("0")
    assert second_summary.negative_balance_month == decimal.Decimal("155.42")
    assert second_summary.positive_current_balance == decimal.Decimal("220.9")
    assert second_summary.negative_current_balance == decimal.Decimal("155.42")
    assert second_summary.month == 4
    assert second_summary.year == 2024
