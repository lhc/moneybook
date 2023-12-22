from django.shortcuts import render

from moneybook.bookkeeping.models import Transaction


def transactions(request, year=None):
    initial_balance = 0

    transactions = Transaction.objects.all()
    if year is not None:
        transactions = Transaction.objects.for_year(year)
        initial_balance = Transaction.objects.initial_balance_for_year(year)

    transactions = transactions.values(
        "reference",
        "date",
        "amount",
        "description",
        "account__name",
        "category__name",
    )

    transactions_balance = 0 + initial_balance
    for transaction in transactions:
        transactions_balance += transaction["amount"]
        transaction["balance"] = transactions_balance

    return render(
        request,
        "bookkeeping/transactions.html",
        context={"transactions": transactions, "initial_balance": initial_balance},
    )
