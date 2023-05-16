from unittest.mock import patch

from psycopg2 import OperationalError as Perror
from django.core.management import call_command 
from django.db.utils import OperationalError
from django.test import SimpleTestCase 

@patch('test_app.managements.commands.wait_for_db.Command.Check')
class CommandTests(SimpleTestCase):

    def test_wait_for_db(self, patched_check):
        patched_check.return_value=True

        call_command('wait_for_db')

        patched_check.assert_call_once_with(databases=['default'])
    @patch('time.sleep')
    def test_wait_for_db_delay(self,patched_sleep, patched_check):
        patched_check.side_effact = [Perror] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_comma, 6)
        patched_check.assert_called_with(databases=['default'])