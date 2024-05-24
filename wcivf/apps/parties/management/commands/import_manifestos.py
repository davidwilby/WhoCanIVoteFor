import csv

from django.core.management.base import BaseCommand
from elections.models import Election
from parties.models import Manifesto, Party


class Command(BaseCommand):
    """
    The 2024 party manifesto list is at:
    https://docs.google.com/spreadsheets/d/e/2PACX-1vS0GJ6wED4d87K1AMXTxxfYl1L-RwjuH-DY1lcwAH9Wj8MChrxPRVDXqc1dzMW8sVdGDLXcBi0usnDl/pub?gid=0&single=true&output=csv
    Download and store it locally, then run this command with:
    manage.py import_manifestos /path/to/csv
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "filename", help="Path to the file with the manifestos"
        )

    def handle(self, **options):
        with open(options["filename"], "r") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                party_id = row["party_id"].strip()
                if "-" in party_id:
                    party_id = "joint-party:" + party_id
                else:
                    party_id = "party:" + party_id

                try:
                    election = Election.objects.get(slug=row["election_id"])
                except Exception:
                    continue
                try:
                    party = Party.objects.get(party_id="%s" % party_id)
                    self.add_manifesto(row, party, election)
                except Party.DoesNotExist:
                    print("Party not found with ID %s" % party_id)

    def add_manifesto(self, row, party, election):
        country = row.get("country", "UK").strip()
        if "local." in election.slug:
            country = "Local"
        language = row.get("language", "English").strip()

        manifesto_web = row["Manifesto Website URL"].strip()
        manifesto_pdf = row["Manifesto PDF URL"].strip()
        easy_read_url = row.get("easy read version", "").strip()
        if any([manifesto_web, manifesto_pdf]):
            manifesto_obj, created = Manifesto.objects.update_or_create(
                election=election,
                party=party,
                country=country,
                language=language,
                defaults={
                    "web_url": manifesto_web,
                    "pdf_url": manifesto_pdf,
                    "easy_read_url": easy_read_url,
                },
            )
            manifesto_obj.save()
