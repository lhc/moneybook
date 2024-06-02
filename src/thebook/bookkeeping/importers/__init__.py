def build_importer(): ...


importers = {
    ("bradesco", "csv"): BradescoCSVImporter,
    ("bradesco", "ofx"): BradescoOFXImporter,
    ("paypal", "csv"): PaypalCSVImporter,
    ("cora", "csv"): CoraCSVImporter,
    ("cora", "ofx"): CoraOFXImporter,
}


@dataclass
class ImportedTransaction:
    reference
    date
    description
    transaction_type
    amount
    cash_book
    category


class BradescoCSVImporter:

    def __init__(self, file, cash_book): ...

    def extract_transactions(self): ...


importer = build_importer(source)
transactions = importer("file.xxx", cash_book).extract_transactions()
