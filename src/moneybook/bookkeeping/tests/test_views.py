import pytest
from django.urls import reverse
from model_bakery import baker

from moneybook.bookkeeping.models import CashBook


@pytest.fixture
def cash_book():
    cash_book = baker.make(CashBook, name="Cash Account", slug="cash-account")
    return cash_book


@pytest.mark.django_db
def test_dashboard_access(client):
    response = client.get(reverse("bookkeeping:dashboard"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_cash_book_all_transactions_access(client, cash_book):
    response = client.get(
        reverse("bookkeeping:cash-book-transactions", args=(cash_book.slug,))
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_cash_book_transactions_for_year_access(client, cash_book):
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


@pytest.mark.django_db
def test_all_transactions_access(client, cash_book):
    response = client.get(reverse("bookkeeping:all-transactions"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_all_transactions_for_year_access(client, cash_book):
    response = client.get(
        reverse("bookkeeping:all-transactions-for-year", args=(2024,))
    )

    assert response.status_code == 200


# @pytest.mark.django_db
# def test_empty_cash_book_transactions(client):
#    cash_book = baker.make(CashBook)
#    response = client.get(reverse("bookkeeping:cash-book-transactions"), args=(cash_book.slug,))
#
#    assert response.status_code == 200
#
#
#
# @pytest.mark.django_db
# def test_can_get_transactions_without_providing_year(client):
#    response = client.get(reverse("bookkeeping:all-transactions"))
#
#    assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_can_get_transactions_by_year(client):
#    response = client.get(reverse("bookkeeping:all-transactions-for-year", args=(2023,)))
#
#    assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_exclude_transaction_of_different_year(client):
#    transaction_2021 = baker.make(Transaction, date=datetime.date(2021, 4, 28))
#    transaction_2022 = baker.make(Transaction, date=datetime.date(2022, 3, 2))
#    transaction_2023 = baker.make(Transaction, date=datetime.date(2023, 12, 8))
#
#    response = client.get(reverse("bookkeeping:all-transactions-for-year", args=(2022,)))
#
#    transactions = response.context.get("transactions") or []
#    assert len(transactions) == 1
#
#    references = [transaction["reference"] for transaction in transactions]
#    assert transaction_2021.reference not in references
#    assert transaction_2022.reference in references
#    assert transaction_2023.reference not in references
#
#
# @pytest.mark.django_db
# def test_year_transactions_should_have_initial_balance_from_previous_years(client):
#    baker.make(
#        Transaction, date=datetime.date(2021, 3, 2), amount=decimal.Decimal("50.0")
#    )
#    baker.make(
#        Transaction, date=datetime.date(2021, 4, 2), amount=decimal.Decimal("60.0")
#    )
#    baker.make(
#        Transaction, date=datetime.date(2022, 4, 2), amount=decimal.Decimal("600.0")
#    )
#    baker.make(
#        Transaction, date=datetime.date(2023, 4, 2), amount=decimal.Decimal("7000.0")
#    )
#
#    response = client.get(reverse("bookkeeping:all-transactions-for-year", args=(2022,)))
#
#    assert "initial_balance" in response.context
#    assert response.context["initial_balance"] == decimal.Decimal("110.0")
#
#
# @pytest.mark.django_db
# def test_no_balance_from_previous_year(client):
#    baker.make(
#        Transaction, date=datetime.date(2021, 3, 2), amount=decimal.Decimal("50.0")
#    )
#
#    response = client.get(reverse("bookkeeping:all-transactions-for-year", args=(2021,)))
#
#    assert "initial_balance" in response.context
#    assert response.context["initial_balance"] == decimal.Decimal("0.0")
#
#
# @pytest.mark.django_db
# def test_no_balance_at_all(client):
#    response = client.get(reverse("bookkeeping:all-transactions"))
#
#    assert "initial_balance" in response.context
#    assert response.context["initial_balance"] == decimal.Decimal("0.0")
