from django.http import HttpResponse


def dashboard(request):
    return HttpResponse("")


def all_transactions(request, year=None):
    return HttpResponse("")


def cash_book_transactions(request, cash_book_slug, year=None):
    return HttpResponse("")


# def cash_book_transactions(request, cash_book_slug):
#    ...
#
#
#
#
#
# def transactions(request, year=None):
#    initial_balance = 0
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
