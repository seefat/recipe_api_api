from django.core.management.base import BaseCommand

import time

from psycopg2 import OperationalError as Psycopg2Operror
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('waiting for database')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up=True
            except(Psycopg2Operror, OperationalError):
                self.stdout.write('Database unavailablse! wait for a second')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database Available!'))
