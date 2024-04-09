import datetime
import decimal

from django.shortcuts import render

from thebook.bookkeeping.models import CashBook, Transaction


def dashboard(request):
    today = datetime.date.today()
    summary = Transaction.objects.summary(month=today.month, year=today.year)
    cash_books = CashBook.objects.all()

    return render(
        request,
        "bookkeeping/dashboard.html",
        context={
            "incomes__current_month": summary.get("incomes__current_month")
            or decimal.Decimal("0"),
            "expenses__current_month": summary.get("expenses__current_month")
            or decimal.Decimal("0"),
            "balance__current_month": summary.get("balance__current_month")
            or decimal.Decimal("0"),
            "balance__current_year": summary.get("balance__current_year")
            or decimal.Decimal("0"),
            "cash_books": cash_books,
        },
    )
