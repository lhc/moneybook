import datetime
import decimal
from dataclasses import dataclass

from django.db import models
from django.db.models import F, Q, Sum, Value, Window


@dataclass
class TransactionSummary:
    incomes_month: decimal.Decimal
    expenses_month: decimal.Decimal
    balance_month: decimal.Decimal
    balance_year: decimal.Decimal
    current_balance: decimal.Decimal
    month: int
    year: int


class CashBookQuerySet(models.QuerySet):
    def summary(self, month, year):
        return self.annotate(
            balance_month=Sum(
                "transaction__amount",
                filter=Q(
                    transaction__date__month=month,
                    transaction__date__year=year,
                ),
                default=decimal.Decimal("0"),
            ),
            current_balance=Sum(
                "transaction__amount",
                default=decimal.Decimal("0"),
            ),
            month=Value(month),
            year=Value(year),
        )


class TransactionQuerySet(models.QuerySet):
    def for_cash_book(self, slug):
        return self.filter(cash_book__slug=slug)

    def for_period(self, month, year):
        return self.filter(date__month=month, date__year=year)

    def initial_balance_for_year(self, year):
        reference_date = datetime.date(year, 1, 1)
        initial_balance = self.filter(date__lt=reference_date).aggregate(
            Sum("amount")
        ).get("amount__sum") or decimal.Decimal("0.0")
        return initial_balance

    def summary(self, month, year):
        incomes_month = self.filter(
            date__month=month, date__year=year, transaction_type=self.model.INCOME
        ).aggregate(incomes_month=Sum("amount"))["incomes_month"] or decimal.Decimal(
            "0"
        )
        expenses_month = self.filter(
            date__month=month, date__year=year, transaction_type=self.model.EXPENSE
        ).aggregate(expenses_month=Sum("amount"))["expenses_month"] or decimal.Decimal(
            "0"
        )

        balance_month = self.filter(
            date__month=month,
            date__year=year,
        ).aggregate(
            balance_month=Sum("amount")
        )["balance_month"] or decimal.Decimal("0")

        balance_year = self.filter(
            date__year=year,
        ).aggregate(
            balance_year=Sum("amount")
        )["balance_year"] or decimal.Decimal("0")

        current_balance = self.filter().aggregate(current_balance=Sum("amount"))[
            "current_balance"
        ] or decimal.Decimal("0")

        return TransactionSummary(
            incomes_month=incomes_month,
            expenses_month=expenses_month,
            balance_month=balance_month,
            balance_year=balance_year,
            current_balance=current_balance,
            month=month,
            year=year,
        )

    def with_cumulative_sum(self):
        return (
            self.order_by("date")
            .order_by("id")
            .annotate(cumulative_sum=Window(Sum("amount"), order_by=F("id").asc()))
        )
