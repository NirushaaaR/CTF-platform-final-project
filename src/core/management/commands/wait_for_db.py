import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """ Django Command to pause till database is available """
    def handle(self, *args, **options):
        self.stdout.write("Waiting for dabase...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable try connect again...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!!"))