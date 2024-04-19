import datetime

from django.shortcuts import render

from thebook.bookkeeping.models import CashBook, Transaction


def dashboard(request):
    today = datetime.date.today()
    transactions_summary = Transaction.objects.summary(
        month=today.month, year=today.year
    )
    cash_books_summary = CashBook.objects.summary(month=today.month, year=today.year)

    return render(
        request,
        "bookkeeping/dashboard.html",
        context={
            "transactions_summary": transactions_summary,
            "cash_books_summary": cash_books_summary,
        },
    )
