from django.urls import path

from moneybook.bookkeeping import views

app_name = "bookkeeping"

urlpatterns = [
    path("", views.transactions, name="transactions"),
    path("<int:year>/", views.transactions, name="year-transactions"),
]
