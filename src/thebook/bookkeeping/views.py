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

    transactions = cash_book.transaction_set.for_period(
        month, year
    ).with_cumulative_sum()

    initial_balance = 0

    return render(
        request,
        "bookkeeping/transactions.html",
        context={
            "cash_book": cash_book,
            "initial_balance": initial_balance,
            "transactions": transactions,
        },
    )
