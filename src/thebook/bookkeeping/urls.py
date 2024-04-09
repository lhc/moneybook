from django.urls import path

from thebook.bookkeeping import views

app_name = "bookkeeping"

urlpatterns = [
    path("all", views.all_transactions, name="all-transactions"),
    path("all/<int:year>", views.all_transactions, name="all-transactions-for-year"),
    path("cb/", views.cash_books, name="cash-books"),
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
