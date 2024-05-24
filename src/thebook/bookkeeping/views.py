from django.http import HttpResponse
from django.shortcuts import render

from thebook.bookkeeping.models import CashBook


def cash_books(request):
    return render(request, "bookkeeping/cashbooks.html")


def all_transactions(request):
    return HttpResponse("All transactions")


def cash_book_transactions(request, cash_book_slug):
    cash_book = CashBook.objects.get(slug=cash_book_slug)
    year = request.GET.get("year") or None
    month = request.GET.get("month") or None

    transactions = cash_book.transaction_set.all().select_related("category")
    if month is not None and year is not None:
        transactions = transactions.for_period(month, year)

    initial_balance = 0

    return render(
        request,
        "bookkeeping/transactions.html",
        context={
            "cash_book": cash_book,
            "initial_balance": initial_balance,
            "transactions": transactions.with_cumulative_sum(),
        },
    )


def import_transactions(request):
    cash_books = CashBook.objects.all().order_by("name")

    return render(
        request, "bookkeeping/import.html", context={"cash_books": cash_books}
    )
