from django.urls import reverse
from model_bakery import baker

from thebook.bookkeeping.models import CashBook


def test_import_transaction_access(client):
    response = client.get(reverse("bookkeeping:import-transactions"))

    assert response.status_code == 200


def test_import_transaction_has_cash_book_list_in_context(client, db):
    cash_book_1 = baker.make(CashBook)
    cash_book_2 = baker.make(CashBook)
    cash_book_3 = baker.make(CashBook)

    response = client.get(reverse("bookkeeping:import-transactions"))

    assert "cash_books" in response.context
    assert cash_book_1 in response.context["cash_books"]
    assert cash_book_2 in response.context["cash_books"]
    assert cash_book_3 in response.context["cash_books"]
