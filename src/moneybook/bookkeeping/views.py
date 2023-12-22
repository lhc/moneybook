from django.shortcuts import render

from moneybook.bookkeeping.models import Transaction


def transactions(request, year=None):
    transactions = Transaction.objects.all()
    if year is not None:
        transactions = Transaction.objects.for_year(year)

    transactions = transactions.values(
        "reference",
        "date",
        "amount",
        "description",
        "account__name",
        "category__name",
    )

    transactions_balance = 0
    for transaction in transactions:
        transactions_balance += transaction["amount"]
        transaction["balance"] = transactions_balance

    return render(
        request, "bookkeeping/transactions.html", context={"transactions": transactions}
    )
