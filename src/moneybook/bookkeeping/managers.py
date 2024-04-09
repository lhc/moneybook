import datetime
import decimal

from django.db import models
from django.db.models import F, Sum, Window


class TransactionQuerySet(models.QuerySet):
    def for_cash_book(self, slug):
        return self.filter(cash_book__slug=slug)

    def for_year(self, year):
        return self.filter(date__year=year)

    def initial_balance_for_year(self, year):
        reference_date = datetime.date(year, 1, 1)
        initial_balance = self.filter(date__lt=reference_date).aggregate(
            Sum("amount")
        ).get("amount__sum") or decimal.Decimal("0.0")
        return initial_balance

    def summary(self, month, year):
        today = datetime.date.today()

        year_transactions = self.filter(date__year=today.year)
        month_transactions = year_transactions.filter(date__month=today.month)

        incomes__current_month = month_transactions.filter(
            transaction_type=self.model.INCOME
        ).aggregate(incomes=Sum("amount")).get("incomes") or decimal.Decimal("0")

        expenses__current_month = month_transactions.filter(
            transaction_type=self.model.EXPENSE
        ).aggregate(expenses=Sum("amount")).get("expenses") or decimal.Decimal("0")

        incomes__current_year = year_transactions.filter(
            transaction_type=self.model.INCOME
        ).aggregate(incomes=Sum("amount")).get("incomes") or decimal.Decimal("0")

        expenses__current_year = year_transactions.filter(
            transaction_type=self.model.EXPENSE
        ).aggregate(expenses=Sum("amount")).get("expenses") or decimal.Decimal("0")

        balance__current_month = incomes__current_month - expenses__current_month
        balance__current_year = incomes__current_year - expenses__current_year

        return {
            "incomes__current_month": incomes__current_month,
            "expenses__current_month": expenses__current_month,
            "balance__current_month": balance__current_month,
            "balance__current_year": balance__current_year,
        }

    def with_cumulative_sum(self):
        return self.order_by("date").annotate(
            cumulative_sum=Window(Sum("amount"), order_by=F("id").asc())
        )
