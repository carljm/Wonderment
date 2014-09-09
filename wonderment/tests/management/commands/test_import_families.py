from unittest import mock

from django.core.management import call_command

from wonderment.tests import factories as f


class TestCommand(object):
    def test_calls_import_csv(self, db):
        session = f.SessionFactory.create()

        with mock.patch('wonderment.import_data.import_csv') as mock_icsv:
            call_command('import_families', 'somefile.csv', str(session.id))

        mock_icsv.assert_called_once_with(session, 'somefile.csv')
