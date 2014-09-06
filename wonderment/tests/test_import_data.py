import csv
import os
import tempfile

from wonderment.import_data import import_csv, FIELDS
from wonderment import models


def do(*rows):
    """Create temp CSV file from given row dicts and import it.

    Given field names should be short versions, will be translated.

    Order of fields is not guaranteed.

    """
    f = tempfile.NamedTemporaryFile(
        prefix='wonderment-tests-tmp-', mode='w', newline='', delete=False)
    try:
        writer = csv.DictWriter(f.file, FIELDS.values())
        writer.writeheader()
        for row in rows:
            translated = {FIELDS[k]: v for k, v in row.items()}
            writer.writerow(translated)
        f.close()
        import_csv(f.name)
    finally:
        os.remove(f.name)


class TestImportCsv(object):
    def test_parent_name(self, db):
        do({'first': "First", 'last': "Last"})

        assert models.Parent.objects.get().name == "First Last"
