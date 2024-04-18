import datetime
import decimal

from django.shortcuts import render

from thebook.bookkeeping.models import CashBook, Transaction


def dashboard(request):
    today = datetime.date.today()
    summary = Transaction.objects.summary(month=today.month, year=today.year)

    cash_books_summary = []
    for cash_book in CashBook.objects.all():
        cash_books_summary.append(cash_book.summary(today.month, today.year))

    return render(
        request,
        "bookkeeping/dashboard.html",
        context={
            "incomes__current_month": summary.get("incomes_month")
            or decimal.Decimal("0"),
            "expenses__current_month": summary.get("expenses_month")
            or decimal.Decimal("0"),
            "balance__current_month": summary.get("balance_month")
            or decimal.Decimal("0"),
            "balance": summary.get("current_balance") or decimal.Decimal("0"),
            "cash_books_summary": cash_books_summary,
        },
    )
