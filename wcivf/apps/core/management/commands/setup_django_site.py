"""
Hack because Django makes it hard to use data migrations to do this :/
"""

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        Site.objects.all().update(domain="whocanivotefor.co.uk")
