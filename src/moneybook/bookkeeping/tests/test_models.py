import datetime

import pytest
from django.db import IntegrityError
from model_bakery import baker

from moneybook.bookkeeping.models import Transaction


@pytest.mark.django_db
def test_default_transaction_retrieval_order_by_date_asc():
    transaction_1 = baker.make(Transaction, date=datetime.date(2023, 4, 28))
    transaction_2 = baker.make(Transaction, date=datetime.date(2023, 3, 2))
    transaction_3 = baker.make(Transaction, date=datetime.date(2023, 10, 8))
    transaction_4 = baker.make(Transaction, date=datetime.date(2023, 4, 10))

    transactions = Transaction.objects.all()

    assert transactions[0] == transaction_2
    assert transactions[1] == transaction_4
    assert transactions[2] == transaction_1
    assert transactions[3] == transaction_3


@pytest.mark.django_db
def test_each_transaction_need_a_unique_reference_value():
    transaction_reference = "123456A"
    transaction_1 = baker.make(Transaction, reference=transaction_reference)  # noqa

    with pytest.raises(IntegrityError):
        transaction_2 = baker.prepare(
            Transaction, reference=transaction_reference, _save_related=True
        )
        transaction_2.save()
