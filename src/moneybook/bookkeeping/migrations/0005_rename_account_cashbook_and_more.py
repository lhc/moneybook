# Generated by Django 5.0 on 2024-02-18 14:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bookkeeping", "0004_alter_transaction_transaction_type"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Account",
            new_name="CashBook",
        ),
        migrations.RenameField(
            model_name="transaction",
            old_name="account",
            new_name="cash_book",
        ),
    ]
