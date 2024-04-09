import datetime
import decimal

from django.http import HttpResponse
from django.shortcuts import render

from moneybook.bookkeeping.models import CashBook, Transaction


def cash_books(request):
    return render(request, "bookkeeping/cashbooks.html")


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


def all_transactions(request, year=None):
    return HttpResponse("All transactions")


def cash_book_transactions(request, cash_book_slug, year=None):
    cash_book = CashBook.objects.get(slug=cash_book_slug)

    transactions = Transaction.objects.for_cash_book(
        cash_book_slug
    ).with_cumulative_sum()
    if year is not None:
        transactions = transactions.for_year(year)

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


#
#
# def transactions(request, year=None):
#
#    transactions = Transaction.objects.all()
#    if year is not None:
#        transactions = Transaction.objects.for_year(year)
#        initial_balance = Transaction.objects.initial_balance_for_year(year)
#
#    transactions = transactions.values(
#        "reference",
#        "date",
#        "amount",
#        "description",
#        "cash_book__name",
#        "category__name",
#    )
#
#    transactions_balance = 0 + initial_balance
#    for transaction in transactions:
#        transactions_balance += transaction["amount"]
#        transaction["balance"] = transactions_balance
#
#    return render(
#        request,
#        "bookkeeping/transactions.html",
#        context={"transactions": transactions, "initial_balance": initial_balance},
#    )
