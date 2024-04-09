import decimal

import pytest
from django.urls import reverse
from model_bakery import baker

from thebook.bookkeeping.models import CashBook, Transaction


@pytest.fixture
def cash_book():
    cash_book = baker.make(CashBook, name="Cash Account", slug="cash-account")
    return cash_book


def test_cash_book_all_transactions_access(db, client, cash_book):
    response = client.get(
        reverse("bookkeeping:cash-book-transactions", args=(cash_book.slug,))
    )

    assert response.status_code == 200


def test_cash_book_transactions_for_year_access(db, client, cash_book):
    response = client.get(
        reverse(
            "bookkeeping:cash-book-transactions-for-year",
            args=(
                cash_book.slug,
                2024,
            ),
        )
    )

    assert response.status_code == 200


def test_all_transactions_access(db, client, cash_book):
    response = client.get(reverse("bookkeeping:all-transactions"))

    assert response.status_code == 200


def test_all_transactions_for_year_access(db, client, cash_book):
    response = client.get(
        reverse("bookkeeping:all-transactions-for-year", args=(2024,))
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_all_transactions_of_cashbook(client, cash_book):
    transaction_1 = baker.make(Transaction, cash_book=cash_book)
    transaction_2 = baker.make(Transaction, cash_book=cash_book)
    transaction_3 = baker.make(Transaction, cash_book=cash_book)

    response = client.get(
        reverse("bookkeeping:cash-book-transactions", args=(cash_book.slug,))
    )

    transactions = response.context.get("transactions") or []
    assert len(transactions) == 3

    assert transaction_1 in transactions
    assert transaction_2 in transactions
    assert transaction_3 in transactions


def test_exclude_transactions_of_other_cash_book(db, client, cash_book):
    cash_book_2 = baker.make(CashBook)

    transaction_1 = baker.make(Transaction, cash_book=cash_book)
    transaction_2 = baker.make(Transaction, cash_book=cash_book_2)

    response = client.get(
        reverse("bookkeeping:cash-book-transactions", args=(cash_book.slug,))
    )

    transactions = response.context.get("transactions") or []
    assert len(transactions) == 1

    assert transaction_1 in transactions
    assert transaction_2 not in transactions


def test_initial_balance_zero(db, client, cash_book):
    response = client.get(
        reverse("bookkeeping:cash-book-transactions", args=(cash_book.slug,))
    )

    assert "initial_balance" in response.context
    assert response.context["initial_balance"] == decimal.Decimal("0.0")


def test_cash_book_on_context(db, client, cash_book):
    response = client.get(
        reverse("bookkeeping:cash-book-transactions", args=(cash_book.slug,))
    )

    assert "cash_book" in response.context
    assert response.context["cash_book"] == cash_book
