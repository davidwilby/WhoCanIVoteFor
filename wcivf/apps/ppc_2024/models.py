from core.utils import LastWord
from django.db import models
from django.db.models import Count, F
from parties.models import Party
from people.models import Person


class PPCPersonQuerySet(models.QuerySet):
    def by_party(self) -> dict:
        return (
            self.all()
            .annotate(name=F("party__party_name"))
            .values("name")
            .annotate(candidate_count=Count("pk"))
            .order_by("name")
        )

    def by_region(self) -> dict:
        # We can't assume that we have a row for each region in the data,
        # so we first make a dict with all the regions, then update
        # that dict with data from the database
        regions = {
            "East Midlands": {"total_seats": 47},
            "Eastern": {"total_seats": 61},
            "London": {"total_seats": 75},
            "North East": {"total_seats": 27},
            "North West": {"total_seats": 73},
            "Northern Ireland": {"total_seats": 18},
            "Scotland": {"total_seats": 57},
            "South East": {"total_seats": 91},
            "South West": {"total_seats": 58},
            "Wales": {"total_seats": 32},
            "West Midlands": {"total_seats": 57},
            "Yorkshire and the Humber": {"total_seats": 54},
        }

        qs = (
            self.all()
            .values("region_name")
            .annotate(candidate_count=Count("pk"))
            .order_by("region_name")
        )
        for region in qs:
            regions[region["region_name"]]["candidate_count"] = region[
                "candidate_count"
            ]

        return regions

    def for_details(self):
        return self.select_related("person", "party")

    # If we want to show previous details, ever
    # def annotate_previously_stood(self):
    #     return self.annotate(
    #         previously_stood=Count("person__personpost"),
    #     )
    # def annotate_previously_elected(self):
    #     return self.annotate(
    #         previously_elected=Count("person__personpost", Q(person__personpost__elected=True)),
    #     )


# Create your models here.
class PPCPerson(models.Model):
    CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRhZbBrU2AdJDYyBZViMs6irvH7zVUiZm2rDoADw5B18drp6hILJBr-duSXCmHJ18SmYWm3iq0bbfoR/pub?gid=0&single=true&output=csv"

    person_name = models.CharField(max_length=255, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    constituency_name = models.CharField(max_length=255)
    region_name = models.CharField(max_length=255, blank=True)
    sheet_row = models.JSONField()

    objects = PPCPersonQuerySet.as_manager()

    class Meta:
        ordering = ("constituency_name", LastWord("person_name"))
