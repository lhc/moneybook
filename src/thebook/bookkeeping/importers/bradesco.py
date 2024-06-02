importer = BradescoImporter(filename)
transactions = importer.get_transactions()

transaction.save()
