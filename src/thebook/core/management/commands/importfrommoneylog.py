import datetime
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from django.core.management.base import BaseCommand

from thebook.bookkeeping.models import CashBook, Category, Transaction
from thebook.users.models import User


@dataclass
class Entry:
    id_: int
    entry_date: str
    value: float
    account: str
    tags: str
    description: str

    @property
    def category(self):
        return self.tags

    @property
    def date(self):
        return datetime.datetime.strptime(self.entry_date, "%Y-%m-%d").date()

    @property
    def reference(self):
        return f"L{self.id_:05}"

    @property
    def transaction_type(self):
        if "transferencia" in self.tags:
            return Transaction.DEPOSIT if self.value >= 0 else Transaction.WITHDRAW
        return Transaction.INCOME if self.value >= 0 else Transaction.EXPENSE


class Command(BaseCommand):
    help = "Import data from legacy financial database"

    def add_arguments(self, parser):
        parser.add_argument("db", type=str)
        parser.add_argument(
            "year",
            nargs="?",
            default=None,
            type=int,
            help="Import only entries of specified year",
        )

    def handle(self, *args, **options):
        db_path = Path(options["db"])
        year = options["year"]

        self.stdout.write(self.style.SUCCESS(f"Processing database {db_path}"))

        if not db_path.is_file():
            self.stdout.write(self.style.ERROR(f"Unable to find {db_path}"))
            return

        if year is not None:
            self.stdout.write(self.style.WARNING(f"Processing entries of year {year}"))

        automation_user, _ = User.objects.get_or_create(email="contato@lhc.net.br")
        cash_books = {cash_book.name: cash_book for cash_book in CashBook.objects.all()}
        categories = {category.name: category for category in Category.objects.all()}

        existing_transactions = Transaction.objects.values_list("reference", flat=True)

        transactions = []

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        results = cursor.execute(
            """
        SELECT
            id, entry_date, value, account, tags, description
        FROM
            entry
        """
        )
        for entry in results:
            legacy_entry = Entry(*entry)

            if legacy_entry.reference in existing_transactions:
                continue

            if legacy_entry.category == "inicial":
                # We don't need to have a transaction for the year start
                continue

            if year is not None and legacy_entry.date.year != year:
                continue

            entry_cash_book = cash_books.get(legacy_entry.account)
            if entry_cash_book is None:
                entry_cash_book = CashBook.objects.create(name=legacy_entry.account)
                cash_books[legacy_entry.account] = entry_cash_book

            entry_category = categories.get(legacy_entry.category)
            if entry_category is None:
                entry_category = Category.objects.create(name=legacy_entry.category)
                categories[legacy_entry.category] = entry_category

            transactions.append(
                Transaction(
                    reference=legacy_entry.reference,
                    date=legacy_entry.entry_date,
                    description=legacy_entry.description,
                    transaction_type=legacy_entry.transaction_type,
                    amount=abs(legacy_entry.value),
                    notes="Imported from legacy bookkeeping system",
                    cash_book=entry_cash_book,
                    category=entry_category,
                    created_by=automation_user,
                )
            )

        self.stdout.write(
            self.style.WARNING(f"Importing {len(transactions)} new transactions")
        )
        Transaction.objects.bulk_create(transactions)
        self.stdout.write(self.style.SUCCESS("Data imported"))
