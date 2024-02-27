from django.urls import path

from moneybook.bookkeeping import views

app_name = "bookkeeping"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("all", views.all_transactions, name="all-transactions"),
    path("all/<int:year>", views.all_transactions, name="all-transactions-for-year"),
    path(
        "cb/<slug:cash_book_slug>",
        views.cash_book_transactions,
        name="cash-book-transactions",
    ),
    path(
        "cb/<slug:cash_book_slug>/<int:year>",
        views.cash_book_transactions,
        name="cash-book-transactions-for-year",
    ),
]
