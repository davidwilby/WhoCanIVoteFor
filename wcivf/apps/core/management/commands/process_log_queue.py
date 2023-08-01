from core.models import write_logged_postcodes
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        write_logged_postcodes()
