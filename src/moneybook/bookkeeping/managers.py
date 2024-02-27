import datetime
import decimal

from django.db import models
from django.db.models import Sum


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
