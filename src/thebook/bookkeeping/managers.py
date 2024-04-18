import datetime
import decimal

from django.db import models
from django.db.models import F, Q, Sum, Value, Window


class CashBookQuerySet(models.QuerySet):
    def summary(self, month, year):
        from thebook.bookkeeping.models import Transaction

        return self.annotate(
            positive_balance_month=Sum(
                "transaction__amount",
                filter=Q(
                    transaction__date__month=month,
                    transaction__date__year=year,
                    transaction__transaction_type__in=(
                        Transaction.DEPOSIT,
                        Transaction.INCOME,
                    ),
                ),
            ),
            negative_balance_month=Sum(
                "transaction__amount",
                filter=Q(
                    transaction__date__month=month,
                    transaction__date__year=year,
                    transaction__transaction_type__in=(
                        Transaction.WITHDRAW,
                        Transaction.EXPENSE,
                    ),
                ),
            ),
            positive_current_balance=Sum(
                "transaction__amount",
                filter=Q(
                    transaction__transaction_type__in=(
                        Transaction.DEPOSIT,
                        Transaction.INCOME,
                    )
                ),
            ),
            negative_current_balance=Sum(
                "transaction__amount",
                filter=Q(
                    transaction__transaction_type__in=(
                        Transaction.WITHDRAW,
                        Transaction.EXPENSE,
                    )
                ),
            ),
            month=Value(month),
            year=Value(year),
        )


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
        all_transactions = self.all()
        year_transactions = all_transactions.filter(date__year=year)
        month_transactions = year_transactions.filter(date__month=month)

        all_summary = all_transactions.aggregate(
            incomes=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.INCOME),
            ),
            expenses=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.EXPENSE),
            ),
            deposits=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.DEPOSIT),
            ),
            withdraws=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.WITHDRAW),
            ),
        )

        year_summary = year_transactions.aggregate(
            incomes=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.INCOME),
            ),
            expenses=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.EXPENSE),
            ),
            deposits=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.DEPOSIT),
            ),
            withdraws=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.WITHDRAW),
            ),
        )

        month_summary = month_transactions.aggregate(
            incomes=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.INCOME),
            ),
            expenses=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.EXPENSE),
            ),
            deposits=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.DEPOSIT),
            ),
            withdraws=Sum(
                "amount",
                default=decimal.Decimal("0"),
                filter=Q(transaction_type=self.model.WITHDRAW),
            ),
        )

        return {
            "incomes_month": month_summary["incomes"],
            "expenses_month": month_summary["expenses"],
            "balance_month": month_summary["incomes"]
            + month_summary["deposits"]
            - month_summary["expenses"]
            - month_summary["withdraws"],
            "balance_year": year_summary["incomes"]
            + year_summary["deposits"]
            - year_summary["expenses"]
            - year_summary["withdraws"],
            "current_balance": all_summary["incomes"]
            + all_summary["deposits"]
            - all_summary["expenses"]
            - all_summary["withdraws"],
            "month": month,
            "year": year,
        }

    def with_cumulative_sum(self):
        return self.order_by("date").annotate(
            cumulative_sum=Window(Sum("amount"), order_by=F("id").asc())
        )
